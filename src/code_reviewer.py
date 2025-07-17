#!/usr/bin/env python3
"""
Code Review Tool for Claude Code

A command-line tool that merges user review requests with a code reviewer prompt
template and calls Claude Code for analysis.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def load_prompt_template():
    """Load the code reviewer prompt template."""
    script_dir = Path(__file__).parent.parent
    prompt_file = script_dir / "prompts" / "code_reviewer_prompt.txt"
    
    if not prompt_file.exists():
        raise FileNotFoundError(f"Prompt template not found at {prompt_file}")
    
    with open(prompt_file, 'r', encoding='utf-8') as f:
        return f.read()


def get_system_prompt_file():
    """Get the path to the system prompt file for file reference."""
    script_dir = Path(__file__).parent.parent
    prompt_file = script_dir / "prompts" / "code_reviewer_prompt.txt"
    
    if not prompt_file.exists():
        raise FileNotFoundError(f"Prompt template not found at {prompt_file}")
    
    return str(prompt_file)


# Claude Code path override (leave empty for default behavior)
CLAUDE_PATH_OVERRIDE = ""


def call_claude_code(system_prompt_file, user_prompt):
    """Call Claude Code with system prompt file reference and user prompt."""
    try:
        # Use command substitution syntax for system prompt
        system_prompt_ref = f"$(<{system_prompt_file})"
        
        if CLAUDE_PATH_OVERRIDE:
            # Use specific path if override is set - need shell=True for command substitution
            cmd = f'{CLAUDE_PATH_OVERRIDE} --append-system-prompt "{system_prompt_ref}" -p'
        else:
            # Use default claude command
            cmd = f'claude --append-system-prompt "{system_prompt_ref}" -p'
        
        
        result = subprocess.run(
            cmd,
            shell=True,
            input=user_prompt,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
            
    except subprocess.CalledProcessError as e:
        print(f"Error calling Claude Code: {e}", file=sys.stderr)
        if e.stderr:
            print(f"Error output: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: 'claude' command not found. Please ensure Claude Code is installed and in PATH.", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Code review tool using Claude Code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "Review the authentication module in src/auth.py"
  %(prog)s "Check error handling in the database connection code"
  %(prog)s "Analyze the test coverage for the payment processing functions"
        """
    )
    
    parser.add_argument(
        "review_request",
        help="Description of what to review (will be appended to the prompt template)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the merged prompt without calling Claude Code"
    )
    
    args = parser.parse_args()
    
    try:
        # Get the system prompt file path
        system_prompt_file = get_system_prompt_file()
        
        # User prompt is just the review request
        user_prompt = args.review_request
        
        if args.dry_run:
            print("System prompt file:")
            print("=" * 50)
            print(f"<@{system_prompt_file}")
            print("\nSystem prompt content:")
            print("=" * 25)
            print(load_prompt_template())
            print("\nUser prompt:")
            print("=" * 20)
            print(user_prompt)
            return
        
        # Call Claude Code with system prompt file and user prompt
        output = call_claude_code(system_prompt_file, user_prompt)
        print(output)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()