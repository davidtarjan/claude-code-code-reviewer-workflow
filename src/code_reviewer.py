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


def merge_prompt(template, user_request):
    """Merge user request with the template prompt."""
    placeholder = "[This section will be appended with specific task details and file paths]"
    
    if placeholder not in template:
        raise ValueError("Template prompt does not contain the expected placeholder")
    
    return template.replace(placeholder, user_request)


# Claude Code path override (leave empty for default behavior)
CLAUDE_PATH_OVERRIDE = ""


def call_claude_code(merged_prompt):
    """Call Claude Code with the merged prompt."""
    try:
        if CLAUDE_PATH_OVERRIDE:
            # Use specific path if override is set
            result = subprocess.run(
                [CLAUDE_PATH_OVERRIDE, "-p"],
                input=merged_prompt,
                capture_output=True,
                text=True,
                check=True
            )
        else:
            # Use default claude command
            result = subprocess.run(
                ["claude", "-p"],
                input=merged_prompt,
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
        # Load the prompt template
        template = load_prompt_template()
        
        # Merge with user request
        merged_prompt = merge_prompt(template, args.review_request)
        
        if args.dry_run:
            print("Merged prompt:")
            print("=" * 50)
            print(merged_prompt)
            return
        
        # Call Claude Code
        output = call_claude_code(merged_prompt)
        print(output)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()