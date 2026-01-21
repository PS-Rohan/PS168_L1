# Weekend Wizard 🧙

A friendly CLI agent that plans chill weekend itineraries using MCP tools and Ollama LLM.

## Features

| Activity | Description | Source |
|----------|-------------|--------|
| **Tell a joke** | Get a funny joke to make you laugh | Serper API |
| **Weather search** | Get current weather for any city | Serper API |
| **Book recommendations** | Suggest great books on any topic | Serper API |
| **Holiday suggestions** | Suggested activities for any destination | Serper API |
| **Random dog photo** | Get a random dog image URL | Dog CEO API |
| **Trivia question** | Get a multiple-choice trivia question | Open Trivia DB |

## Setup

### 1. Configure Environment
Create a `.env` file in the root directory:
```env
SERPER_API_KEY=your_serper_api_key_here
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Ollama and Pull Model
Download Ollama from [ollama.com](https://ollama.com), then:
```bash
ollama pull mistral:7b
```

## Usage

### Test Individual Tools
```bash
python test_tools.py
```

### Run the Agent
```bash
python agent_fun.py
```

## Architecture
The agent uses a ReAct-style loop with Ollama (Mistral). It connects to a Python-based MCP tools server via stdio. All secrets are managed via `.env`.

## Files
- `server_fun.py`: MCP tools server.
- `agent_fun.py`: Agent client.
- `test_tools.py`: Comprehensive test suite.
- `.env`: API keys and configuration.
- `requirements.txt`: Python dependencies.
