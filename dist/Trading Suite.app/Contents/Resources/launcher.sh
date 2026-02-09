#!/bin/bash
# This script is launched by "TradingSuite" executable via Terminal.app
# It runs in a full user context, bypassing App Sandboxing issues.

# 1. Determine Project Root (Up 3 levels from Resources: .../dist/Trading Suite.app/Contents/Resources -> .../dist -> Project Root is up one more level?? NO.)
# Bundle: dist/Trading Suite.app/Contents/Resources/launcher.sh
# ../../../.. -> Project Root
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$DIR/../../../.."

cd "$PROJECT_ROOT"

# Set Terminal Title
echo -n -e "\033]0;Trading Suite\007"

echo "=================================================="
echo "🚀 Starting Trading Suite (Terminal Mode)..."
echo "=================================================="
echo "📂 Project Root: $(pwd)"

# 2. Check/Create Venv
echo "🔧 Checking Environment..."
if [ ! -d "venv" ]; then
    echo "⚠️  Creating virtual environment..."
    if command -v python3.12 &> /dev/null; then
        python3.12 -m venv venv
    else
        echo "❌ Python 3.12 not found. Please install it."
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

source venv/bin/activate

# Always check/install dependencies to ensure updates are applied
echo "📦 Checking dependencies..."
pip install -r requirements.txt

# 3. Launch App
echo "✅ Environment Active."
echo "🌟 Launching Home.py..."
streamlit run Home.py

# Keep window open on exit
echo "❌ App exited."
read -p "Press Enter to close..."
