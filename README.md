# Company Intelligence Platform

An advanced agentic AI system designed to conduct deep research on companies, extract key entities, map their relationships, and generate comprehensive intelligence reports. This project utilizes the **CrewAI** framework for orchestration, **Ollama** for local LLM inference, and **Serper API** for real-time web search.

## 🚀 Features

-   **Deep Web Research**: Autonomous agents scour the web for the latest company information.
-   **Entity Extraction**: Identifies Products, Key People, Locations, and Competitors.
-   **Relationship Mapping**: Connects entities to understand the company's ecosystem (e.g., "Person A is the CEO of Company X").
-   **Local Privacy**: Uses local LLMs (via Ollama) for processing, ensuring data privacy.
-   **Structured Reporting**: Generates professional Markdown reports ready for executive review.

## 🛠️ Technology Stack

-   **Framework**: [CrewAI](https://crewai.com) (Multi-agent orchestration).
-   **LLM Integration**: [LangChain](https://langchain.com) & [Ollama](https://ollama.com).
-   **Search Tool**: [Serper Dev](https://serper.dev) (Google Search API).
-   **Language**: Python 3.10+.

## 📋 Prerequisites

1.  **Python 3.10** or higher.
2.  **Ollama**: Installed and running locally.
    -   Download from [ollama.com](https://ollama.com).
    -   Run `ollama serve`.
    -   Pull the model: `ollama pull qwen:latest`.
3.  **Serper API Key**: A free API key from [serper.dev](https://serper.dev).

## ⚙️ Installation & Setup

1.  **Clone/Navigate to the directory**:
    ```bash
    cd company_intelligence
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment**:
    -   Rename `.env.example` to `.env`.
    -   Add your API keys and configuration:
    ```ini
    SERPER_API_KEY=your_api_key_here
    OLLAMA_BASE_URL=http://localhost:11434
    OLLAMA_MODEL=qwen:latest
    ```

## 🏃 Usage

Run the main script with the name of the company you want to research:

```bash
python main.py --company "Tesla"
```

### What Happens Next?
1.  **Researcher Agent** searches for mission, products, news, etc.
2.  **Entity Extractor** identifies structured data points.
3.  **Relationship Mapper** analyzes connections.
4.  **Report Writer** compiles `company_intelligence_report.md`.

## 📂 Project Structure

```
company_intelligence/
├── src/
│   ├── agents.py       # Agent definitions (Researcher, Extractor, etc.)
│   ├── tasks.py        # Task definitions and prompts
│   └── config.py       # Configuration and Env management
├── main.py             # Entry point script
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
└── README.md           # This file
```

## 📄 Output

The system generates a `company_intelligence_report.md` file containing:
-   Executive Summary
-   Company Overview
-   Key Entities Table (Products, People, Locations, Competitors)
-   Relationship Analysis
-   Recent Developments
