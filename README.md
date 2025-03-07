# DeepSeek Reasoner CLI

An interactive command-line interface for interacting with DeepSeek's AI models, featuring a rich terminal UI with syntax highlighting, parameter customization, and conversation history.

## Features

- Interactive parameter configuration
- Enhanced terminal UI with [Rich](https://github.com/Textualize/rich)
- Syntax highlighting for code blocks
- Markdown rendering
- Conversation history viewing
- On-the-fly parameter editing

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd <repository-directory>
```

2. Install dependencies:
```bash
pip install openai rich python-dotenv
```

3. Create a `.env` file in the project root with your DeepSeek API key:
```
DEEPSEEK_API_KEY=your_api_key_here
```

## Usage

### Basic Usage
```bash
python r1.py
```

### Run with Custom Parameters
```bash
python r1.py --temperature 0.7 --max_tokens 2000
```

### Skip Interactive Configuration
```bash
python r1.py --no-interactive
```

### Special Commands During Chat
- `params`: Edit parameters for the next API call
- `history`: View the conversation history
- `exit`: End the conversation

## Development

This project is organized as a single script for ease of use. Future improvements could include:
- Breaking down into modules for better organization
- Adding support for multiple models
- Implementing conversation saving and loading
- Adding more UI customization options

## License

MIT