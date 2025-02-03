## Natural Language iMessage Search

### Overview

This is a simple Python Gradio based app that allows you to search your iMessage history using natural language. Messages are never sent to any inference servers or any servers through this script. iMessages are stored in a `chat.db` which can be queried with regular sqlite3, and this app will only use LLM to generate the query. It will run the query directly on your local machine.

#### Assumptions

- You are using a Mac
- Your iMessage history is stored in `~/Library/Messages/chat.db`
- You have an OpenRouter API key (see https://openrouter.ai)

### Installation

```bash
# Start venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Setup

Create a `.env` file and add your OpenRouter API key:

```bash
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

If you want to use another model (the default is `anthropic/claude-3.5-sonnet`), you can set the `MODEL` environment variable:

```bash
MODEL=openai/gpt-4o-mini
```

### Usage

```bash
sudo python app.py
```

### Demo

<tbd>
