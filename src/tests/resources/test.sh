#!/bin/bash

# Test script for the Minibook Action
# This script simulates the action by running the minibook command with test inputs

# Set up test inputs
TITLE="Test Minibook"
DESCRIPTION="This is a test minibook created by the test script"
OUTPUT="."
FORMAT="html"
# Multiline JSON string — valid, no escaped line continuations
LINKS='{
  "GitHub": "https://github.com",
  "Python": "https://python.org"
}'
#LINKS='{"GitHub": "https://github.com", "Python": "https://python.org"}'

# Install minibook if not already installed
if ! command -v minibook &> /dev/null; then
    echo "Installing minibook..."
    uv pip install minibook
fi

# Run the minibook command
echo "Creating minibook with the following inputs:"
echo "Title: $TITLE"
echo "Description: $DESCRIPTION"
echo "Output: $OUTPUT"
echo "Format: $FORMAT"
echo "Links: $LINKS"
echo ""

uv run minibook \
    --title "$TITLE" \
    --description "$DESCRIPTION" \
    --output "$OUTPUT" \
    --format "$FORMAT" \
    --links "$LINKS"

# Check if the minibook was created successfully
if [ -f "$OUTPUT/index.html" ]; then
    echo "Minibook created successfully at $OUTPUT/index.html"
    exit 0
else
    echo "Failed to create minibook"
    exit 1
fi
