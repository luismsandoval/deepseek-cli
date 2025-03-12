#!/usr/bin/env python3
# Please install dependencies first: `pip install openai rich python-dotenv`

from openai import OpenAI
import argparse
import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Rich library imports for enhanced UI
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.prompt import Prompt, Confirm
from rich.table import Table

# Initialize Rich console
console = Console()

# Default parameter values and their descriptions
DEFAULT_PARAMS = {
    "temperature": {
        "value": 1.0,
        "help": "Controls randomness of output. Lower is more deterministic, higher is more creative.",
        "recommendations": "Coding/Math: 0.0, Data Analysis: 1.0, General: 1.3, Translation: 1.3, Creative: 1.5",
        "type": float,
        "min": 0.0,
        "max": 2.0
    },
    "max_tokens": {
        "value": 4000,
        "help": "Maximum number of tokens in the response",
        "type": int,
        "min": 1,
        "max": 8000
    },
    "top_p": {
        "value": 1.0,
        "help": "Controls diversity via nucleus sampling",
        "type": float,
        "min": 0.0,
        "max": 1.0
    },
    "frequency_penalty": {
        "value": 0.0,
        "help": "Penalizes repeated tokens",
        "type": float,
        "min": -2.0,
        "max": 2.0
    },
    "presence_penalty": {
        "value": 0.0,
        "help": "Penalizes tokens already present in text",
        "type": float,
        "min": -2.0,
        "max": 2.0
    },
    "api_key": {
        "value": os.getenv("DEEPSEEK_API_KEY", ""),
        "help": "DeepSeek API key (from .env file)",
        "type": str
    },
    "base_url": {
        "value": "https://api.deepseek.com",
        "help": "DeepSeek API base URL",
        "type": str
    },
    "model": {
        "value": "deepseek-reasoner",
        "help": "Model to use",
        "type": str
    },
    "system_message": {
        "value": "You are a helpful assistant, focused on the field of AI and machine learning, sort of like my personal programming tutor.",
        "help": "System message that defines the assistant's behavior and knowledge",
        "type": str
    }
}

# Setup argument parser for customization
def setup_args():
    parser = argparse.ArgumentParser(description='DeepSeek Reasoner CLI')
    
    # Model parameters
    parser.add_argument('--temperature', type=float, default=DEFAULT_PARAMS["temperature"]["value"],
                        help=DEFAULT_PARAMS["temperature"]["help"])
    parser.add_argument('--max_tokens', type=int, default=DEFAULT_PARAMS["max_tokens"]["value"],
                        help=DEFAULT_PARAMS["max_tokens"]["help"])
    parser.add_argument('--top_p', type=float, default=DEFAULT_PARAMS["top_p"]["value"],
                        help=DEFAULT_PARAMS["top_p"]["help"])
    parser.add_argument('--frequency_penalty', type=float, default=DEFAULT_PARAMS["frequency_penalty"]["value"],
                        help=DEFAULT_PARAMS["frequency_penalty"]["help"])
    parser.add_argument('--presence_penalty', type=float, default=DEFAULT_PARAMS["presence_penalty"]["value"],
                        help=DEFAULT_PARAMS["presence_penalty"]["help"])
    
    # API settings
    parser.add_argument('--api_key', type=str, default=DEFAULT_PARAMS["api_key"]["value"],
                        help=DEFAULT_PARAMS["api_key"]["help"])
    parser.add_argument('--base_url', type=str, default=DEFAULT_PARAMS["base_url"]["value"],
                        help=DEFAULT_PARAMS["base_url"]["help"])
    parser.add_argument('--model', type=str, default=DEFAULT_PARAMS["model"]["value"],
                        help=DEFAULT_PARAMS["model"]["help"])
    parser.add_argument('--system_message', type=str, default=DEFAULT_PARAMS["system_message"]["value"],
                        help=DEFAULT_PARAMS["system_message"]["help"])
    
    # UI flag
    parser.add_argument('--no-interactive', action='store_true',
                        help='Disable interactive parameter configuration')
    
    return parser.parse_args()

# Display and configure parameters interactively
def interactive_config(args) -> Dict[str, Any]:
    console.clear()
    console.print(Panel.fit(
        "[bold blue]DeepSeek Reasoner CLI[/bold blue] - [yellow]Interactive Parameter Configuration[/yellow]",
        border_style="blue"
    ))
    
    # Convert args to dictionary
    params = vars(args).copy()
    
    # Remove the no-interactive flag
    if "no_interactive" in params:
        del params["no_interactive"]
    
    # Display current parameters in a table
    table = Table(title="Current Parameters")
    table.add_column("Parameter", style="cyan")
    table.add_column("Value", style="green")
    table.add_column("Description", style="yellow")
    
    for name, value in params.items():
        if name in DEFAULT_PARAMS:
            table.add_row(
                name,
                str(value),
                DEFAULT_PARAMS[name]["help"]
            )
    
    console.print(table)
    console.print()
    
    if Confirm.ask("Would you like to modify any parameters?"):
        while True:
            # Create a list of parameter names
            param_names = list(params.keys())
            
            # Ask which parameter to edit
            console.print("[bold]Which parameter would you like to modify?[/bold]")
            for i, name in enumerate(param_names):
                console.print(f"[cyan]{i+1}.[/cyan] {name} [green]({params[name]})[/green]")
            console.print(f"[cyan]{len(param_names)+1}.[/cyan] Done editing")
            
            choice = Prompt.ask(
                "Enter your choice",
                choices=[str(i+1) for i in range(len(param_names)+1)],
                default=str(len(param_names)+1)
            )
            
            if int(choice) == len(param_names)+1:
                break
                
            param_name = param_names[int(choice)-1]
            param_info = DEFAULT_PARAMS[param_name]
            
            # Get current value
            current_value = params[param_name]
            
            # Show parameter details
            console.print(f"\n[bold]{param_name}[/bold]")
            console.print(f"Description: {param_info['help']}")
            
            if "recommendations" in param_info:
                console.print(f"Recommendations: {param_info['recommendations']}")
                
            if "min" in param_info and "max" in param_info:
                console.print(f"Range: {param_info['min']} to {param_info['max']}")
            
            # Get new value
            if param_info["type"] == float:
                new_value = float(Prompt.ask(
                    f"Enter new value for {param_name}",
                    default=str(current_value)
                ))
                
                # Constrain to min/max if specified
                if "min" in param_info and new_value < param_info["min"]:
                    new_value = param_info["min"]
                if "max" in param_info and new_value > param_info["max"]:
                    new_value = param_info["max"]
                    
            elif param_info["type"] == int:
                new_value = int(Prompt.ask(
                    f"Enter new value for {param_name}",
                    default=str(current_value)
                ))
                
                # Constrain to min/max if specified
                if "min" in param_info and new_value < param_info["min"]:
                    new_value = param_info["min"]
                if "max" in param_info and new_value > param_info["max"]:
                    new_value = param_info["max"]
                    
            else:  # String
                new_value = Prompt.ask(
                    f"Enter new value for {param_name}",
                    default=str(current_value)
                )
                
            # Update parameter
            params[param_name] = new_value
            console.print(f"[green]Updated {param_name} to {new_value}[/green]\n")
            
    console.clear()
    console.print(Panel.fit(
        "[bold blue]DeepSeek Reasoner CLI[/bold blue] - [green]Configuration Complete[/green]",
        border_style="blue"
    ))
    
    # Display final parameters
    table = Table(title="Final Parameters")
    table.add_column("Parameter", style="cyan")
    table.add_column("Value", style="green")
    
    for name, value in params.items():
        table.add_row(name, str(value))
        
    console.print(table)
    console.print()
    
    return params

# Helper function to display markdown content with code highlighting
def display_markdown(content, title=None, style="green"):
    # Create a panel with the markdown content
    md = Markdown(content)
    
    if title:
        console.print(Panel(md, title=title, border_style=style))
    else:
        console.print(md)

# Helper function to detect and parse code blocks in markdown
def extract_code_blocks(content):
    import re
    
    # Find all code blocks in the markdown
    # They follow the pattern: ```language\ncode\n```
    code_block_pattern = r"```(\w*)\n(.*?)```"
    code_blocks = re.findall(code_block_pattern, content, re.DOTALL)
    
    return code_blocks

# Helper function to display a response with proper formatting
def display_response(content, title, style="green"):
    # Check if the content contains code blocks
    code_blocks = extract_code_blocks(content)
    
    # If there are code blocks, display them with syntax highlighting
    if code_blocks:
        # Replace code blocks with placeholders for processing
        placeholder_pattern = "__CODE_BLOCK_{}_PLACEHOLDER__"
        processed_content = content
        
        for i, (language, code) in enumerate(code_blocks):
            placeholder = placeholder_pattern.format(i)
            block_pattern = f"```{language}\n{code}```"
            processed_content = processed_content.replace(block_pattern, placeholder)
        
        # Split by placeholders
        parts = processed_content.split("__CODE_BLOCK_")
        
        # Display the first part (if any)
        if parts[0]:
            display_markdown(parts[0])
        
        # Process and display each part with its code block
        for i, part in enumerate(parts[1:], 0):
            if "_PLACEHOLDER__" in part:
                index_str, remaining = part.split("_PLACEHOLDER__", 1)
                index = int(index_str)
                language, code = code_blocks[index]
                
                # If language is empty, default to "text"
                if not language:
                    language = "text"
                
                # Display the code block with syntax highlighting
                console.print(Syntax(code.strip(), language, theme="monokai", line_numbers=True))
                
                # Display remaining text if any
                if remaining:
                    display_markdown(remaining)
    else:
        # If no code blocks, just display as markdown
        display_markdown(content, title, style)

# Function to handle the conversation parameters configuration
def edit_parameters(params):
    # Create a copy of the parameters
    updated_params = params.copy()
    
    # Display current parameters
    table = Table(title="Current Parameters")
    table.add_column("Parameter", style="cyan")
    table.add_column("Value", style="green")
    
    for name, value in updated_params.items():
        if name in DEFAULT_PARAMS:  # Only show parameters relevant to the API
            table.add_row(name, str(value))
    
    console.print(table)
    
    # Ask which parameter to edit
    if Confirm.ask("Would you like to modify any parameters for this message?"):
        param_names = [name for name in updated_params.keys() if name in DEFAULT_PARAMS]
        
        while True:
            console.print("[bold]Which parameter would you like to modify?[/bold]")
            for i, name in enumerate(param_names):
                console.print(f"[cyan]{i+1}.[/cyan] {name} [green]({updated_params[name]})[/green]")
            console.print(f"[cyan]{len(param_names)+1}.[/cyan] Done editing")
            
            choice = Prompt.ask(
                "Enter your choice",
                choices=[str(i+1) for i in range(len(param_names)+1)],
                default=str(len(param_names)+1)
            )
            
            if int(choice) == len(param_names)+1:
                break
                
            param_name = param_names[int(choice)-1]
            param_info = DEFAULT_PARAMS[param_name]
            
            # Get current value
            current_value = updated_params[param_name]
            
            # Show parameter details
            console.print(f"\n[bold]{param_name}[/bold]")
            console.print(f"Description: {param_info['help']}")
            
            if "recommendations" in param_info:
                console.print(f"Recommendations: {param_info['recommendations']}")
                
            if "min" in param_info and "max" in param_info:
                console.print(f"Range: {param_info['min']} to {param_info['max']}")
            
            # Get new value based on type
            if param_info["type"] == float:
                new_value = float(Prompt.ask(
                    f"Enter new value for {param_name}",
                    default=str(current_value)
                ))
                
                # Constrain to min/max if specified
                if "min" in param_info and new_value < param_info["min"]:
                    new_value = param_info["min"]
                if "max" in param_info and new_value > param_info["max"]:
                    new_value = param_info["max"]
                    
            elif param_info["type"] == int:
                new_value = int(Prompt.ask(
                    f"Enter new value for {param_name}",
                    default=str(current_value)
                ))
                
                # Constrain to min/max if specified
                if "min" in param_info and new_value < param_info["min"]:
                    new_value = param_info["min"]
                if "max" in param_info and new_value > param_info["max"]:
                    new_value = param_info["max"]
                    
            else:  # String
                new_value = Prompt.ask(
                    f"Enter new value for {param_name}",
                    default=str(current_value)
                )
                
            # Update parameter
            updated_params[param_name] = new_value
            console.print(f"[green]Updated {param_name} to {new_value}[/green]\n")
    
    return updated_params

# Helper function to display the conversation history
def display_history(messages):
    console.clear()
    console.print(Panel.fit(
        "[bold blue]DeepSeek Reasoner CLI[/bold blue] - [yellow]Conversation History[/yellow]",
        border_style="blue"
    ))
    
    # Skip the system message
    for i, message in enumerate(messages):
        if message["role"] == "system":
            continue
            
        if message["role"] == "user":
            console.print(Panel(
                message["content"],
                title=f"[bold cyan]User (Message {i})[/bold cyan]",
                border_style="cyan",
                padding=(1, 2)
            ))
        else:  # assistant
            display_response(
                message["content"],
                f"[bold green]Assistant (Response {i})[/bold green]",
                "green"
            )
    
    console.print("\n[bold]Press Enter to return to the conversation[/bold]")
    Prompt.ask("")  # Wait for user to press Enter

# Main function
def main():
    args = setup_args()
    
    # Run interactive configuration if not disabled
    if not args.no_interactive:
        params = interactive_config(args)
    else:
        params = vars(args)
    
    # Initialize OpenAI client with API key
    client = OpenAI(api_key=params["api_key"], base_url=params["base_url"])
    
    # Initialize the conversation with the system message
    messages = [
        {"role": "system", "content": params["system_message"]}
    ]
    
    # Display welcome message and instructions
    console.print(Panel.fit(
        f"[bold blue]DeepSeek Reasoner CLI[/bold blue] - [yellow]Model: {params['model']}[/yellow]",
        subtitle="Type 'exit' to end the conversation, 'params' to edit parameters, 'system' to edit system message, 'history' to view conversation",
        border_style="blue"
    ))
    
    # Main conversation loop
    while True:
        # Display parameter edit prompt and message input in different colors
        console.print("\n[bold cyan]Enter your message[/bold cyan] ([italic]Type 'params' to edit parameters, 'system' to edit system message, 'history' to view conversation, or 'exit' to quit[/italic]):")
        user_input = Prompt.ask("")
        
        # Check for special commands
        if user_input.lower() == 'exit':
            console.print("[yellow]Conversation ended.[/yellow]")
            break
        elif user_input.lower() == 'params':
            params = edit_parameters(params)
            continue
        elif user_input.lower() == 'system':
            current_system = messages[0]["content"]
            console.print(f"\n[bold magenta]Current system message:[/bold magenta]\n{current_system}")
            new_system = Prompt.ask("\n[bold magenta]Enter new system message[/bold magenta]", default=current_system)
            messages[0]["content"] = new_system
            params["system_message"] = new_system
            console.print("[green]System message updated successfully![/green]")
            continue
        elif user_input.lower() == 'history':
            display_history(messages)
            continue
        
        # Add user message to conversation history
        messages.append({"role": "user", "content": user_input})
        
        # Show "thinking" status
        with console.status("[bold green]Thinking...[/bold green]", spinner="dots"):
            try:
                # Send the conversation to the API with customized parameters
                response = client.chat.completions.create(
                    model=params["model"],
                    messages=messages,
                    temperature=params["temperature"],
                    max_tokens=params["max_tokens"],
                    top_p=params["top_p"],
                    frequency_penalty=params["frequency_penalty"],
                    presence_penalty=params["presence_penalty"],
                    stream=False
                )
                
                # Extract the reasoning content and final answer
                # Handle case where reasoning_content might not be present in the response
                reasoning_content = getattr(response.choices[0].message, 'reasoning_content', 'No reasoning provided')
                final_answer = response.choices[0].message.content
                
                # Display chain of thought reasoning
                console.print("\n[bold magenta]Chain of Thought:[/bold magenta]")
                display_response(reasoning_content, "Chain of Thought", "magenta")
                
                # Display final answer
                console.print("\n[bold green]Final Answer:[/bold green]")
                display_response(final_answer, "Final Answer", "green")
                
                # Add ONLY the final answer to the conversation history (not the reasoning_content)
                messages.append({"role": "assistant", "content": final_answer})
                
            except Exception as e:
                console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
                # Remove the last user message since we couldn't get a response
                messages.pop()

if __name__ == "__main__":
    main()
