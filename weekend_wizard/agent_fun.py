# agent_fun.py
"""
Weekend Wizard Agent Client
A friendly CLI agent that plans weekend itineraries using MCP tools and Ollama LLM.

Features:
- Connects to MCP tools server via stdio
- 6 showcase tools: tell_joke, get_weather, recommend_books, 
  get_holiday_suggestions, random_dog_photo, get_trivia
"""

import asyncio
import json
import sys
import os
import time
from datetime import datetime
from typing import Dict, Any, List
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from ollama import chat  # pip install ollama

LOG_PREFIX = "[AGENT-LOG]"

def log(*msg):
    """Log messages with a prefix for easy filtering."""
    print(LOG_PREFIX, *msg)

SYSTEM = """
You are a cheerful Weekend Wizard assistant with 6 special tools:

1. tell_joke - Get a funny joke (no args)
2. get_weather - Get weather for a city (args: city)
3. recommend_books - Get book recommendations (args: topic)
4. get_holiday_suggestions - Travel ideas (args: destination)
5. random_dog_photo - Get a random dog image (no args)
6. get_trivia - Get a trivia question (no args)

Use the EXACT tool names and argument names shown above.

If using a tool, respond ONLY with valid JSON:
{"action":"tool","name":"tell_joke","args":{}}
{"action":"tool","name":"random_dog_photo","args":{}}
{"action":"tool","name":"get_trivia","args":{}}
{"action":"tool","name":"get_weather","args":{"city":"London"}}
{"action":"tool","name":"recommend_books","args":{"topic":"mystery"}}
{"action":"tool","name":"get_holiday_suggestions","args":{"destination":"Bali"}}

After receiving tool results, provide a fun, friendly final answer:
{"action":"final","answer":"Here's what I found..."}

Always respond with valid JSON. Never include extra text.
"""


def mcp_to_ollama_tool(t):
    """Convert MCP tool schema to Ollama's tool format."""
    return {
        "type": "function",
        "function": {
            "name": t.name,
            "description": t.description or "",
            "parameters": t.inputSchema or {"type": "object", "properties": {}}
        }
    }


def llm_json(messages: List[Dict[str, str]], tools: list[dict[str, Any]]) -> Dict[str, Any]:
    """Get JSON response from LLM with native tool support and auto-repair."""
    log("Sending prompt to LLM:")
    print(json.dumps(messages[-1], indent=2))
    log("Available tools passed:", [t["function"]["name"] for t in tools])

    resp = chat(
        model="mistral:7b",
        messages=messages,
        options={"temperature": 0.6, "top_p": 0.9, "top_k": 40},
        tools=tools,
        format="json"
    )

    txt = resp["message"]["content"]
    log("Raw LLM output (string):")
    print(json.dumps(txt, indent=2))

    try:
        parsed = json.loads(txt)
        
        # Handle array of tool calls
        if isinstance(parsed, list):
            if len(parsed) > 0 and isinstance(parsed[0], dict):
                first_call = parsed[0]
                if "action" not in first_call:
                    if "name" in first_call and "args" in first_call:
                        first_call["action"] = "tool"
                return first_call
        
        # Ensure we have an action field
        if "action" not in parsed:
            log("WARNING: LLM response missing 'action' field")
            if "name" in parsed and "args" in parsed:
                parsed["action"] = "tool"
            elif "answer" in parsed:
                parsed["action"] = "final"
        return parsed
    except Exception as e:
        log("ERROR: LLM returned invalid JSON:", e)
        log("Attempting auto-fix...")

        fix = chat(
            model="mistral:7b",
            messages=[
                {"role": "system", "content": "Return ONLY valid JSON with an 'action' field set to either 'tool' or 'final'."},
                {"role": "user", "content": f"Fix this JSON: {txt}"}
            ],
            options={"temperature": 0},
            format="json"
        )

        fix_txt = fix["message"]["content"]
        log("Fixed JSON:")
        print(fix_txt)
        
        try:
            return json.loads(fix_txt)
        except Exception as fix_error:
            log("ERROR: Failed to fix JSON:", fix_error)
            return {"action": "final", "answer": f"I encountered an error processing your request."}


async def main():
    server_path = sys.argv[1] if len(sys.argv) > 1 else "server_fun.py"
    log(f"Starting MCP server using: python {server_path}")

    exit_stack = AsyncExitStack()
    stdio = await exit_stack.enter_async_context(
        stdio_client(StdioServerParameters(command="python", args=[server_path]))
    )
    r_in, w_out = stdio
    session = await exit_stack.enter_async_context(ClientSession(r_in, w_out))

    log("Initializing MCP session")
    await session.initialize()

    tools = (await session.list_tools()).tools
    tool_index = {t.name: t for t in tools}
    ollama_tools = [mcp_to_ollama_tool(t) for t in tools]

    print("=" * 60)
    print("WEEKEND WIZARD - Your Chill Weekend Planner!")
    print("=" * 60)
    print("\nWhat can I help you with today?")
    print("  1. Tell me a joke")
    print("  2. Weather search for any city")
    print("  3. Book recommendations")
    print("  4. Holiday & travel suggestions")
    print("  5. Show me a random dog photo")
    print("  6. Give me a trivia question")
    print("-" * 60)
    log("Connected tools:", list(tool_index.keys()))
    print("\nType your request (or 'exit' to quit):")

    os.makedirs("interactions", exist_ok=True)
    history = [{"role": "system", "content": SYSTEM}]

    try:
        while True:
            user = input("\nYou: ").strip()
            if not user or user.lower() in {"exit", "quit"}:
                print("\nHave a great weekend! 🎉")
                break

            interaction_data = {
                "timestamp": datetime.now().isoformat(),
                "user_prompt": user,
                "tool_calls": [],
                "final_answer": ""
            }

            history.append({"role": "user", "content": user})

            for cycle in range(6):
                log(f"\n--- Decision cycle {cycle+1} ---")
                decision = llm_json(history, ollama_tools)
                log("Decoded LLM JSON decision:")
                print(json.dumps(decision, indent=2))

                if decision.get("action") == "final":
                    answer = decision.get("answer", "")
                    print(f"\nWizard: {answer}")
                    history.append({"role": "assistant", "content": answer})
                    interaction_data["final_answer"] = answer
                    break

                tname = decision.get("name")
                args = decision.get("args", {})

                if not tname or tname not in tool_index:
                    log(f"ERROR: Unknown tool: {tname}")
                    history.append({"role": "user", "content": f"Error: Tool '{tname}' unknown."})
                    continue

                log(f"Calling tool: {tname}")
                try:
                    result = await session.call_tool(tname, args)
                    payload = result.content[0].text if result.content else result.model_dump_json()
                    
                    interaction_data["tool_calls"].append({"tool": tname, "args": args, "result": payload})
                    
                    history.append({
                        "role": "user", 
                        "content": f"Tool '{tname}' returned: {payload}. Now provide a final answer."
                    })
                except Exception as e:
                    log(f"ERROR: {e}")
                    history.append({"role": "user", "content": f"Error: {e}"})

            filename = f"interactions/interaction_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(interaction_data, f, indent=2)

    finally:
        await exit_stack.aclose()


if __name__ == "__main__":
    asyncio.run(main())
