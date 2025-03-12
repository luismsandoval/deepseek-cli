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
git clone https://github.com/luismsandoval/deepseek-cli.git
cd deepseek-cli
```

2. Install dependencies:
```bash
pip install openai rich python-dotenv boto3
```

3. Create a `.env` file in the project root with your DeepSeek API key:
```
DEEPSEEK_API_KEY=your_api_key_here
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_S3_BUCKET=your_s3_bucket_name
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
- `save`: Save conversation to AWS S3 (planned)
- `load`: Load conversation from AWS S3 (planned)
- `exit`: End the conversation

## Development

This project is organized as a single script for ease of use. Future improvements could include:
- Breaking down into modules for better organization
- Adding support for multiple models
- Implementing conversation saving and loading with AWS S3
- Adding more UI customization options

### AWS Integration Plan

#### AWS S3 for Conversation Storage
- Save conversation history to S3 buckets for persistence
- Retrieve past conversations from S3 using unique identifiers
- Implement automatic backups of conversation data
- Add conversation metadata for searchability

Implementation steps:
1. Add boto3 dependency for AWS SDK
2. Create S3 bucket configuration in environment variables
3. Implement save/load functions for conversations
4. Add CLI commands for managing stored conversations

## License

MIT