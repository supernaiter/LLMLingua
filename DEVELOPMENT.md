# Development Guide for LLMLingua-JP

This document provides instructions for setting up the development environment and contributing to LLMLingua-JP.

## 🚀 Quick Setup

### Prerequisites
- Python 3.9+ (recommended: 3.10)
- Git
- pip

### Environment Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/LLMLingua-jp.git
   cd LLMLingua-jp
   ```

2. **Run the setup script**
   ```bash
   chmod +x setup_dev.sh
   ./setup_dev.sh
   ```

   This script will:
   - Create a virtual environment (`.venv`)
   - Install all dependencies
   - Download NLTK data
   - Run basic tests

3. **Activate the environment**
   ```bash
   source .venv/bin/activate
   ```

## 🧪 Running Tests

### All Tests
```bash
make test
```

### Specific Test Files
```bash
# Japanese tokenizer tests
python -m pytest tests/test_tokenizer_jp.py -v

# Japanese prompt compression tests
python -m pytest tests/test_prompt_compressor_jp.py -v

# All tests with coverage
python -m pytest --cov=llmlingua tests/ -v
```

### Code Quality
```bash
# Format code
make style

# Or manually
black llmlingua tests
isort llmlingua tests
flake8 llmlingua tests
```

## 📁 Project Structure

```
LLMLingua-jp/
├── llmlingua/
│   ├── __init__.py
│   ├── prompt_compressor.py    # Main compression logic
│   ├── tokenizer_jp.py         # Japanese tokenization
│   └── utils.py
├── tests/
│   ├── test_tokenizer_jp.py    # Japanese tokenizer tests
│   ├── test_prompt_compressor_jp.py  # Japanese compression tests
│   └── test_llmlingua.py       # Original tests
├── requirements-dev.txt         # Development dependencies
├── setup_dev.sh                 # Setup script
└── .vscode/settings.json        # VS Code configuration
```

## 🔧 Development Workflow

### 1. Feature Development
- Create a feature branch: `git checkout -b feature/japanese-support`
- Make your changes
- Add tests for new functionality
- Run tests: `make test`
- Format code: `make style`

### 2. Testing Strategy
- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test the full compression pipeline
- **Backward Compatibility**: Ensure English functionality still works

### 3. Code Quality
- Follow PEP 8 style guidelines
- Use type hints
- Add docstrings for all public functions
- Keep functions small and focused

## 🌸 Japanese Text Processing

### Tokenization
The Japanese tokenizer uses `fugashi` with `unidic-lite` dictionary:

```python
from llmlingua.tokenizer_jp import tokenize_jp, is_japanese_text

# Tokenize Japanese text
tokens = tokenize_jp("自然言語処理は人工知能の一分野です。")
# Result: "自然言語処理 は 人工知能 の 一分野 です 。"

# Detect Japanese text
is_jp = is_japanese_text("Hello 世界！")
# Result: False (threshold-based detection)
```

### Integration with PromptCompressor
Japanese support is integrated into the main `compress_prompt` method:

```python
from llmlingua import PromptCompressor

compressor = PromptCompressor()

# Automatic detection
result = compressor.compress_prompt(
    context=["日本語のテキスト"],
    lang="auto"
)

# Explicit Japanese processing
result = compressor.compress_prompt(
    context=["日本語のテキスト"],
    lang="ja"
)
```

## 🐛 Debugging

### Common Issues

1. **CUDA/GPU Issues**
   - Use `device_map="cpu"` for testing
   - Ensure PyTorch is installed correctly

2. **Japanese Dependencies**
   - Install with: `pip install fugashi unidic-lite`
   - Check if unidic-lite is downloaded correctly

3. **Tokenization Issues**
   - Test with simple Japanese text first
   - Check Unicode character ranges

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)

from llmlingua.tokenizer_jp import tokenize_jp
result = tokenize_jp("テストテキスト")
```

## 📦 Packaging

### Building
```bash
python setup.py sdist bdist_wheel
```

### Testing Installation
```bash
pip install -e .
python -c "from llmlingua import PromptCompressor; print('Success!')"
```

## 🤝 Contributing

### Pull Request Process
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add/update tests
5. Ensure all tests pass
6. Update documentation
7. Submit a pull request

### Code Review Checklist
- [ ] Tests pass
- [ ] Code is formatted (black, isort)
- [ ] No linting errors (flake8)
- [ ] Documentation updated
- [ ] Backward compatibility maintained

## 🔗 Useful Commands

```bash
# Development environment
source .venv/bin/activate

# Run specific test
python -m pytest tests/test_tokenizer_jp.py::TestJapaneseTokenizer::test_tokenizer_initialization -v

# Check code coverage
python -m pytest --cov=llmlingua --cov-report=html tests/

# Install in development mode
pip install -e .

# Clean up
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

## 📚 Additional Resources

- [LLMLingua Original Paper](https://aclanthology.org/2023.emnlp-main.825/)
- [Fugashi Documentation](https://github.com/polm/fugashi)
- [UniDic Documentation](https://unidic.ninjal.ac.jp/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html) 