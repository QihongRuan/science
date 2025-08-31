#!/bin/bash

# HTML to PDF conversion script using Chrome
# Note: This script uses Chrome's headless mode to convert HTML to PDF

INPUT_HTML="$1"
OUTPUT_PDF="${2:-${INPUT_HTML%.html}_fixed.pdf}"

if [ -z "$INPUT_HTML" ]; then
    echo "Usage: $0 <input.html> [output.pdf]"
    exit 1
fi

if [ ! -f "$INPUT_HTML" ]; then
    echo "Error: Input file $INPUT_HTML does not exist"
    exit 1
fi

# Use Chrome headless to convert HTML to PDF
if [ -d "/Applications/Google Chrome.app" ]; then
    CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
elif [ -d "/Applications/Chromium.app" ]; then
    CHROME="/Applications/Chromium.app/Contents/MacOS/Chromium"
else
    echo "Error: Chrome or Chromium not found"
    exit 1
fi

echo "Converting $INPUT_HTML to $OUTPUT_PDF..."
"$CHROME" --headless --disable-gpu --print-to-pdf="$OUTPUT_PDF" "file://$INPUT_HTML"

if [ $? -eq 0 ]; then
    echo "Successfully created: $OUTPUT_PDF"
else
    echo "Error: Failed to create PDF"
    exit 1
fi