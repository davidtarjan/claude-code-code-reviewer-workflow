# Claude Code Review Workflow

Example how to use Claude Code to review code written by itself. This doesn't eliminate the need for you to review diffs, but does seem to catch cases where CC left out something or went way off track. Best to give it the plan / request / prompt that you gave your CC task as part of the review request, so it knows what the goal was.

## Overview

The tool combines a code reviewer prompt template with user-specific review requests, then calls Claude Code to perform detailed code analysis.

## Components

- `prompts/code_reviewer_prompt.txt` - Comprehensive code reviewer prompt template
- `src/code_reviewer.py` - Python CLI tool that merges prompts and calls Claude Code

## Installation

1. Ensure Claude Code is installed and available in your PATH
2. Clone this repository
3. Make the script executable (already done):
   ```bash
   chmod +x src/code_reviewer.py
   ```

## Usage

### Basic Usage

```bash
python3 src/code_reviewer.py "Review the authentication module in src/auth.py"
```

### Examples

```bash
# Review specific file
python3 src/code_reviewer.py "Check error handling in the database connection code in db/connection.py"

# Review test coverage
python3 src/code_reviewer.py "Analyze the test coverage for the payment processing functions in tests/test_payments.py"

# Review security aspects
python3 src/code_reviewer.py "Security review of user input validation in controllers/user_controller.py"

# Review entire feature implementation
python3 src/code_reviewer.py "Complete review of the new authentication system including src/auth.py, tests/test_auth.py, and related middleware"
```

### Dry Run Mode

Use `--dry-run` to see the merged prompt without executing:

```bash
python3 src/code_reviewer.py --dry-run "Review error handling in API endpoints"
```

## Requirements

- Python 3.6+
- Claude Code CLI tool installed and configured
- Access to the prompt template file

## Troubleshooting

If you encounter issues with the `claude` command not being found or using the wrong version:

1. **Path Issues**: Edit `src/code_reviewer.py` and set `CLAUDE_PATH_OVERRIDE` to the full path of your Claude Code installation:
   ```python
   CLAUDE_PATH_OVERRIDE = "/path/to/your/claude"
   ```

2. **Find Your Claude Path**: Use `which claude` or `type claude` to locate your installation

3. **Multiple Installations**: If you have multiple Claude installations, the override ensures you use the correct one

