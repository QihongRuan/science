#!/bin/bash

# Create clean PDF without header/footer using Chrome's print options
# This script generates a PDF suitable for submission

INPUT_HTML="$1"
OUTPUT_PDF="${2:-${INPUT_HTML%.html}_submission.pdf}"

if [ -z "$INPUT_HTML" ]; then
    echo "Usage: $0 <input.html> [output.pdf]"
    exit 1
fi

if [ ! -f "$INPUT_HTML" ]; then
    echo "Error: Input file $INPUT_HTML does not exist"
    exit 1
fi

# Use Chrome headless to convert HTML to PDF with no headers/footers
if [ -d "/Applications/Google Chrome.app" ]; then
    CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
elif [ -d "/Applications/Chromium.app" ]; then
    CHROME="/Applications/Chromium.app/Contents/MacOS/Chromium"
else
    echo "Error: Chrome or Chromium not found"
    exit 1
fi

echo "Creating clean PDF for submission: $OUTPUT_PDF..."

# Chrome options:
# --print-to-pdf: Generate PDF
# --no-pdf-header-footer: Remove default headers and footers
# --headless: Run without GUI
# --disable-gpu: Disable GPU hardware acceleration
"$CHROME" \
    --headless \
    --disable-gpu \
    --no-pdf-header-footer \
    --print-to-pdf="$OUTPUT_PDF" \
    "file://$INPUT_HTML"

if [ $? -eq 0 ]; then
    echo "Successfully created submission-ready PDF: $OUTPUT_PDF"
    ls -lh "$OUTPUT_PDF"
else
    echo "Error: Failed to create PDF"
    exit 1
fi