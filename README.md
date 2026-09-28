# NEXORA

A private, local AI chatbot built with Python, Streamlit and Ollama. NEXORA streams replies in a clean Dark/Light interface, addresses you by name, and runs entirely on your own machine, so no API keys are needed and your data stays private.

## Features

- **Streaming chat** with chat bubbles, role icons and a typing indicator
- **Personalized replies**: NEXORA asks for your name and uses it
- **Model auto-detection**: lists your installed Ollama models
- **Creativity control**: slider to make replies more precise or more creative
- **File context**: attach a `.txt` or `.md` file for NEXORA to use when answering
- **Session tools**: start a new chat or export the conversation as a text file
- **Themes**: Dark and Light modes with a custom red accent
- **Clear error handling**: live connection status and setup instructions if Ollama or a model is missing

## Requirements

- Python 3.10 or newer
- [Ollama](https://ollama.com) installed
- At least one Ollama model (default: `llama3.2`)
- Python packages listed in `requirements.txt`

Hardware: about 4 GB of RAM for `llama3.2` (8 GB recommended). A GPU is optional but makes replies much faster.

## Installation

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Download a model
ollama pull llama3.2
```

## Usage

```bash
# Make sure Ollama is running (the desktop app usually starts it automatically)
ollama serve

# Launch NEXORA
streamlit run nexora_chatbot.py
```

Then open the local URL shown in the terminal (usually http://localhost:8501).

## Project Structure

```
nexora/
├── nexora_chatbot.py   # Main application
├── requirements.txt    # Python dependencies
└── README.md
```

## Configuration

Most settings are in the sidebar:

| Setting | Description |
|---|---|
| Profile | The name NEXORA uses to address you |
| Ollama host | Change this if Ollama runs elsewhere (default `http://localhost:11434`) |
| Model | Choose from your installed Ollama models |
| Creativity | Controls response randomness (0.0 to 1.5) |
| Context | Attach a `.txt` or `.md` file (first 8,000 characters are used) |
| Theme | Switch between Dark and Light |

To change NEXORA's personality, edit `SYSTEM_PROMPT` at the top of `nexora_chatbot.py`.

## Troubleshooting

| Problem | Fix |
|---|---|
| "Ollama offline" in the header | Run `ollama serve`, then click **Refresh models** |
| "No models installed" | Run `ollama pull llama3.2`, then click **Refresh models** |
| First reply is slow | The model is loading into memory; later replies are faster |
| Empty reply | Try again or pick a different model (some reasoning models return no visible text) |

## Tech Stack

Python · Streamlit · Ollama · Custom CSS
