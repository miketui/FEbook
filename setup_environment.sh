#!/bin/bash
# Revised Setup script for EPUB processing environment

# Exit immediately if a command exits with a non-zero status.
set -e

echo "----------------------------------------------------"
echo "Starting EPUB Processing Environment Setup..."
echo "----------------------------------------------------"

# 1. Create necessary project directories
echo "1. Creating project directories: src, output, temp, validation_reports..."
mkdir -p src output temp validation_reports
echo "   Directories created/ensured."

# 2. Install Python dependencies from requirements.txt
echo "2. Installing Python dependencies from requirements.txt..."
if [ -f requirements.txt ]; then
    # Use 'pip3' for explicit Python 3, common in many environments
    pip install -r requirements.txt
    echo "   Python dependencies installed successfully."
else
    echo "Error: requirements.txt not found in the current directory."
    echo "Please ensure 'requirements.txt' exists with all necessary Python packages."
    exit 1 # Exit if requirements.txt is missing
fi

# 3. Check for essential external tools (e.g., pandoc, if used)
#    Codex environments often have many tools pre-installed.
#    You might need to check if pandoc is available or provide installation steps if it's not.
echo "3. Checking for essential external tools..."

# Check for pandoc (used for conversions to DOCX)
if ! command -v pandoc &> /dev/null; then
    echo "   'pandoc' not found. Installing via apt-get..."
    apt-get update -y >/dev/null
    apt-get install -y pandoc >/dev/null
    echo "   pandoc installed: $(pandoc --version | head -n 1)"
else
    echo "   pandoc found: $(pandoc --version | head -n 1)"
fi

# You might also want to check for epubcheck, a crucial EPUB validator
# epubcheck is a Java application. It's often run externally or manually.
# For simplicity, we'll just inform the user if it's not explicitly installed here.
# If you want to integrate it, you'd need Java installed and then download/run epubcheck.jar
# if ! command -v java &> /dev/null
# then
#     echo "   Warning: 'java' command not found. 'epubcheck' requires Java."
# else
#     echo "   Java found: $(java -version 2>&1 | head -n 1)"
#     # You could add logic here to download/install epubcheck.jar if you automate it
#     # e.g., if [ ! -d "epubcheck" ]; then wget ... unzip ...; fi
# fi

echo "----------------------------------------------------"
echo "Environment setup complete!"
echo "----------------------------------------------------"
echo ""
echo "Next steps for your EPUB workflow:"
echo "----------------------------------------------------"
echo "1.  Place your raw text or Markdown content files into the 'src/' directory."
echo "    (e.g., 'src/chapter1.md', 'src/introduction.txt')"
echo ""
echo "2.  **Examine Content:** Run the examination script to identify issues."
echo "    Example: python src/examine_content.py src/your_book_content/ > validation_reports/examine_log.txt"
echo ""
echo "3.  **Correct Content:** Manually or semi-automatically apply corrections."
echo "    The 'src/correct_content.py' script would contain functions for this."
echo ""
echo "4.  **Validate Files:** Run structural and compliance validation."
echo "    Example: python src/validate_files.py src/processed_html_files/ --output-report validation_reports/validation_report.json"
echo ""
echo "5.  **Compile EPUB:** Assemble all validated content into a professional EPUB."
echo "    Example: python src/compile_epub.py --input-dir src/ --output-file output/my_bestseller.epub --metadata-file src/metadata.json"
echo "----------------------------------------------------"
echo "Remember to check 'validation_reports/' for logs and reports."
echo "Good luck with your EPUB creation!"
echo "----------------------------------------------------"
