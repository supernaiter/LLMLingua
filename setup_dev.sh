#!/bin/bash
# Development environment setup script for LLMLingua-JP

set -e

echo "🚀 Setting up LLMLingua-JP development environment..."

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
echo "📋 Python version: $python_version"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip and install wheel
echo "⬆️  Upgrading pip and installing wheel..."
pip install --upgrade pip wheel

# Install development dependencies
echo "📚 Installing development dependencies..."
pip install -r requirements-dev.txt

# Install package in editable mode
echo "🔗 Installing package in editable mode..."
pip install -e .

# Download NLTK data
echo "📥 Downloading NLTK data..."
python -c "import nltk; nltk.download('punkt_tab')"

# Run basic tests
echo "🧪 Running basic tests..."
python -m pytest tests/test_tokenizer_jp.py -v

echo "✅ Development environment setup complete!"
echo ""
echo "To activate the environment:"
echo "  source .venv/bin/activate"
echo ""
echo "To run tests:"
echo "  make test"
echo ""
echo "To format code:"
echo "  make style" 