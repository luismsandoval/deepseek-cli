# CLAUDE.md - DeepSeek Reasoner CLI

## Commands
- Run application: `python r1.py`
- Run with custom parameters: `python r1.py --temperature 0.7 --max_tokens 2000`
- Run without interactive mode: `python r1.py --no-interactive`
- Set custom system message: `python r1.py --system_message "Your custom system message here"`
- Install dependencies: `pip install openai rich python-dotenv`

## Code Style Guidelines
- **Imports**: Group imports by standard library, external libraries, then local modules
- **Formatting**: Use 4-space indentation and snake_case for variables/functions
- **Types**: Use typing module for type hints (Dict, Any, etc.)
- **Error Handling**: Use try/except blocks with specific exception types
- **Documentation**: Include docstrings for functions with parameter descriptions
- **Constants**: Define constants at module level in UPPER_CASE
- **UI Components**: Use Rich library for terminal UI enhancements
- **Parameters**: Store configuration in dictionaries with metadata
- **Environment**: Use dotenv for environment variable management

## Project Structure
Single-file architecture for simplicity, with potential future modularization.