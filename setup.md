# Voice Prompt Agent Setup

## Prerequisites

1. **OpenRouter API Key**: Get your API key from [OpenRouter](https://openrouter.ai/)
2. **Python 3.7+**: Ensure Python is installed

## Installation

1. **Create virtual environment** (using uv as preferred):
```bash
uv venv voice-prompt-env
source voice-prompt-env/bin/activate
```

2. **Install dependencies**:
```bash
uv pip install -r requirements.txt
```

3. **Set API key**:
```bash
export OPENROUTER_API_KEY="your_api_key_here"
```

Or add to your `.bashrc`/`.zshrc`:
```bash
echo 'export OPENROUTER_API_KEY="your_api_key_here"' >> ~/.bashrc
```

## Usage

### Interactive Mode
```bash
python voice_prompt_agent.py
```

### List Available Prompts
```bash
python voice_prompt_agent.py --list
```

### Process Specific Prompt
```bash
python voice_prompt_agent.py --process ai-transcript
```

### Custom Directories
```bash
python voice_prompt_agent.py --voice-dir custom-voice-dir --output-dir custom-output-dir
```

## Features

- **STT Cleanup**: Removes speech artifacts and mistranscriptions
- **Text Enhancement**: Fixes typos, adds punctuation and paragraphs
- **AI Optimization**: Formats text for optimal LLM parsing
- **Context Preservation**: Maintains detail while removing redundancy
- **Prompt Enrichment**: Adds summary tables and structure
- **LLM Recommendations**: Suggests optimal models for the processed prompt

## Output

Processed prompts are saved in `voice-prompt/processed/` with:
- Timestamp in filename
- Metadata (processing date, model used, tokens)
- Enhanced markdown formatting
