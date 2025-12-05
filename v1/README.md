# FinCat v1.0 - Hebrew Credit Card Automation

Automate Hebrew credit card expense categorization using AI.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure API key
cp config/.env.example config/.env
# Edit config/.env and add your ANTHROPIC_API_KEY

# 3. Run FinCat
python -m fincat.main
```

## Usage

**Watch Mode (continuous):**
```bash
python -m fincat.main
```

**Manual Mode (process once):**
```bash
python -m fincat.main --manual
```

## Features

- ✅ Automatic file detection and processing
- ✅ Hebrew text support (UTF-8)
- ✅ AI categorization (97% accuracy)
- ✅ Supports .xls and .xlsx formats
- ✅ Cross-platform (Mac + Windows)
- ✅ Cost-efficient (< $0.01 per file)

## Structure

```
v1/
├── fincat/              # Main package (9 modules)
├── config/              # Configuration files
├── tests/               # Unit tests
├── requirements.txt     # Dependencies
└── README.md           # This file
```

## Documentation

See main project README for complete documentation.

## License

MIT License
