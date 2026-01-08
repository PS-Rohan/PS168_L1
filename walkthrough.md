# Company Intelligence Platform - Execution Walkthrough

This guide details the step-by-step process to set up and run the Company Intelligence Platform.

## Prerequisites

1.  **Python 3.10+**: Ensure Python is installed.
2.  **Ollama**: Download and install from [ollama.com](https://ollama.com).
3.  **Serper API Key**: Get a free API key from [serper.dev](https://serper.dev).

## Step 1: Install Ollama & Pull Model

The system uses the `qwen` model by default (configurable).

open a terminal and run:
```bash
ollama serve
```

In a **new** terminal window, pull the model:
```bash
ollama pull qwen:latest
```

## Step 2: Set Project Directory

Navigate to the project folder:
```bash
cd c:\Users\RohanChowdhury\Pictures\3e-llm-judge\company_intelligence
```

## Step 3: Configure Environment

1.  Copy the example environment file:
    ```bash
    # Windows Command Prompt
    copy .env.example .env
    ```
2.  Open `.env` in a text editor.
3.  Paste your Serper API Key:
    ```ini
    SERPER_API_KEY=your_actual_api_key_starts_with_apple...
    ```
    *Note: `OLLAMA_BASE_URL` and `OLLAMA_MODEL` are pre-set but can be changed if needed.*

## Step 4: Install Dependencies

Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Step 5: Run the Application

Run the main script with the target company name:

```bash
python main.py --company "NVIDIA"
```

## Step 6: View Results

1.  **Console Output**: You will see the agents working in real-time (Researching -> Extracting -> Mapping -> Reporting).
2.  **Final Report**: Once finished, a file named `company_intelligence_report.md` will be generated in the same directory.

---

## Troubleshooting

-   **Connection Refused**: Ensure `ollama serve` is running in a separate terminal.
-   **Model Not Found**: Run `ollama list` to check if `qwen:latest` is available. If not, run `ollama pull qwen`.
-   **API Error**: Check your `SERPER_API_KEY` in the `.env` file.
