#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Check if API key is provided as argument
if [ "$1" ]; then
  export ANTHROPIC_API_KEY="$1"
  echo "API key set from command line argument"
else
  # Prompt for API key if not provided
  read -p "Enter your Anthropic API key (press Enter to skip Claude integration): " api_key
  if [ "$api_key" ]; then
    export ANTHROPIC_API_KEY="$api_key"
    echo "API key set from input"
  else
    echo "No API key provided. Claude integration will be disabled."
  fi
fi

# Start the web UI
python web_ui.py 