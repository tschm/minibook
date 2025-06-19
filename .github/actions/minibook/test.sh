#!/bin/bash

# Test script for the Minibook Action
# This script simulates the action by running the minibook command with test inputs

# Set up test inputs
TITLE="Test Minibook"
DESCRIPTION="This is a test minibook created by the test script"
OUTPUT="test-minibook.html"
FORMAT="html"
LINKS="GitHub;https://github.com,Python;https://python.org"

# Install minibook if not already installed
if ! command -v minibook &> /dev/null; then
    echo "Installing minibook..."
    pip install minibook
fi

# Run the minibook command
echo "Creating minibook with the following inputs:"
echo "Title: $TITLE"
echo "Description: $DESCRIPTION"
echo "Output: $OUTPUT"
echo "Format: $FORMAT"
echo "Links: $LINKS"
echo ""

minibook \
    --title "$TITLE" \
    --description "$DESCRIPTION" \
    --output "$OUTPUT" \
    --format "$FORMAT" \
    --links "$LINKS"

# Check if the minibook was created successfully
if [ -f "$OUTPUT" ]; then
    echo "Minibook created successfully at $OUTPUT"
    exit 0
else
    echo "Failed to create minibook"
    exit 1
fi