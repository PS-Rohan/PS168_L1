# server_fun.py
"""
MCP Tools Server for Weekend Wizard
Exposes showcase tools powered by Serper API and other public APIs.

Tools:
- tell_joke: Search for jokes (Serper)
- get_weather: Get weather for a city (Serper)
- recommend_books: Get book recommendations (Serper)
- get_holiday_suggestions: Suggest holiday activities (Serper)
- random_dog_photo: Get a random dog image (Dog CEO API)
- get_trivia: Get a random trivia question (Open Trivia DB)
"""

import json
import os
import http.client
import requests
import html
from typing import Dict, Any
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# SSL certificate settings
os.environ["REQUESTS_CA_BUNDLE"] = r""
os.environ["SSL_CERT_FILE"] = r""

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def log(*msg):
    """Log messages with a prefix for easy filtering."""
    print("[SERVER-LOG]", *msg)

mcp = FastMCP("FunTools")


def internet_search(query: str, num_results: int = 5) -> Dict[str, Any]:
    """
    Internal function: Search the internet using Serper API.
    """
    log(f"[internet_search] Query: {query}")
    
    if not SERPER_API_KEY:
        log("ERROR: SERPER_API_KEY not found in environment")
        return {"error": "API Key missing"}

    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({"q": query, "num": num_results})
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    
    try:
        conn.request("POST", "/search", payload, headers)
        res = conn.getresponse()
        data = res.read()
        result = json.loads(data.decode("utf-8"))
        conn.close()
        
        return {
            "query": query,
            "organic": [
                {"title": r.get("title"), "snippet": r.get("snippet"), "link": r.get("link")}
                for r in result.get("organic", [])[:num_results]
            ],
            "answer_box": result.get("answerBox"),
            "knowledge_graph": result.get("knowledgeGraph")
        }
    except Exception as e:
        log(f"ERROR: {e}")
        return {"error": str(e)}


# ========== SHOWCASE TOOLS ==========

@mcp.tool()
def tell_joke() -> Dict[str, Any]:
    """
    Get a funny joke to make you laugh.
    """
    log("Tool called: tell_joke")
    result = internet_search("funny clean joke of the day", num_results=3)
    
    if "error" in result:
        return {"error": result["error"]}
    
    jokes = []
    for item in result.get("organic", []):
        snippet = item.get("snippet", "")
        if snippet:
            jokes.append({
                "source": item.get("title", "Unknown"),
                "joke": snippet
            })
    
    return {
        "tool": "tell_joke",
        "powered_by": "Serper API",
        "jokes": jokes
    }


@mcp.tool()
def get_weather(city: str) -> Dict[str, Any]:
    """
    Get current weather for any city.
    Args:
        city: Name of the city.
    """
    log(f"Tool called: get_weather for city={city}")
    result = internet_search(f"current weather in {city} today", num_results=3)
    
    if "error" in result:
        return {"error": result["error"]}
    
    weather_info = {
        "city": city,
        "tool": "get_weather",
        "powered_by": "Serper API"
    }
    
    answer_box = result.get("answer_box")
    if answer_box:
        weather_info["quick_answer"] = answer_box.get("answer") or answer_box.get("snippet")
    
    weather_info["results"] = [
        {"source": item.get("title", ""), "info": item.get("snippet", "")}
        for item in result.get("organic", [])
    ]
    
    return weather_info


@mcp.tool()
def recommend_books(topic: str) -> Dict[str, Any]:
    """
    Get book recommendations on any topic.
    Args:
        topic: Topic or genre for book recommendations.
    """
    log(f"Tool called: recommend_books for topic={topic}")
    result = internet_search(f"best {topic} books recommendations 2024", num_results=5)
    
    if "error" in result:
        return {"error": result["error"]}
    
    books = []
    for item in result.get("organic", []):
        books.append({
            "source": item.get("title", ""),
            "recommendation": item.get("snippet", ""),
            "link": item.get("link", "")
        })
    
    return {
        "topic": topic,
        "tool": "recommend_books",
        "powered_by": "Serper API",
        "recommendations": books
    }

@mcp.tool()
def get_holiday_suggestions(destination: str) -> Dict[str, Any]:
    """
    Get holiday and travel activity suggestions for a destination.
    Args:
        destination: Travel destination (e.g., "Paris", "Bali Hawaii").
    """
    log(f"Tool called: get_holiday_suggestions for destination={destination}")
    result = internet_search(f"top holiday activities and things to do in {destination}", num_results=5)
    
    if "error" in result:
        return {"error": result["error"]}
    
    suggestions = []
    for item in result.get("organic", []):
        suggestions.append({
            "title": item.get("title", ""),
            "description": item.get("snippet", ""),
            "link": item.get("link", "")
        })
    
    return {
        "destination": destination,
        "tool": "get_holiday_suggestions",
        "powered_by": "Serper API",
        "suggestions": suggestions
    }

@mcp.tool()
def random_dog_photo() -> Dict[str, Any]:
    """
    Get a random dog image URL from Dog CEO API.
    """
    log("Tool called: random_dog_photo")
    try:
        r = requests.get("https://dog.ceo/api/breeds/image/random", verify=False, timeout=10)
        r.raise_for_status()
        data = r.json()
        return {
            "tool": "random_dog_photo",
            "image_url": data.get("message"),
            "status": "success",
            "powered_by": "Dog CEO API"
        }
    except Exception as e:
        log(f"ERROR: {e}")
        return {"error": str(e)}

@mcp.tool()
def get_trivia() -> Dict[str, Any]:
    """
    Get a random multiple-choice trivia question from Open Trivia DB.
    """
    log("Tool called: get_trivia")
    try:
        r = requests.get("https://opentdb.com/api.php?amount=1&type=multiple", verify=False, timeout=10)
        r.raise_for_status()
        data = r.json().get("results", [])
        if not data:
            return {"error": "No trivia found"}
        
        q = data[0]
        # Unescape HTML entities
        question = html.unescape(q.get("question", ""))
        correct = html.unescape(q.get("correct_answer", ""))
        incorrect = [html.unescape(x) for x in q.get("incorrect_answers", [])]
        
        return {
            "tool": "get_trivia",
            "category": q.get("category"),
            "difficulty": q.get("difficulty"),
            "question": question,
            "correct_answer": correct,
            "incorrect_answers": incorrect,
            "powered_by": "Open Trivia DB"
        }
    except Exception as e:
        log(f"ERROR: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    mcp.run()  # stdio server
