#!/bin/bash

# Setup script for Gemini-Powered UI Design Assistant

echo "🎨 Swim Stroke Analyzer - UI Design Assistant Setup"
echo "=================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Install required package
echo "📦 Installing google-generativeai package..."
pip3 install google-generativeai

if [ $? -eq 0 ]; then
    echo "✅ Package installed successfully"
else
    echo "❌ Failed to install package"
    exit 1
fi

echo ""
echo "🔑 API Key Setup"
echo "==============="
echo ""

# Check if API key is already set
if [ -z "$GEMINI_API_KEY" ]; then
    echo "GEMINI_API_KEY is not set."
    echo ""
    echo "To get your API key:"
    echo "1. Visit: https://makersuite.google.com/app/apikey"
    echo "2. Sign in with your Google account"
    echo "3. Click 'Create API Key'"
    echo "4. Copy your API key"
    echo ""
    read -p "Enter your Gemini API key (or press Enter to skip): " api_key

    if [ -n "$api_key" ]; then
        export GEMINI_API_KEY="$api_key"
        echo "✅ API key set for this session"
        echo ""
        echo "To make it permanent, add this to your ~/.zshrc or ~/.bashrc:"
        echo "export GEMINI_API_KEY='$api_key'"
    else
        echo "⚠️  Skipped API key setup. You'll need to set it before running the assistant."
        echo "Run: export GEMINI_API_KEY='your-key-here'"
    fi
else
    echo "✅ GEMINI_API_KEY is already set"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Make sure GEMINI_API_KEY is set: echo \$GEMINI_API_KEY"
echo "2. Run the design assistant: python3 design_assistant.py"
echo "3. Review results in design_recommendations/"
echo ""
echo "For detailed instructions, see: UI_DESIGN_GUIDE.md"
