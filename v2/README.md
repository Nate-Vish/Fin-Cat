# FinCat v2.0 - Hebrew Credit Card Automation

**Automate your Hebrew credit card expense tracking using AI.**

FinCat watches a folder for Hebrew credit card statements (.xls/.xlsx), automatically categorizes each transaction using Claude AI, and maintains a master Excel file with all your expenses.

---

## ✨ What's New in v2

- ✅ **Robust Parsing**: Handles diverse Israeli bank formats (tested with Amex, Cal, Leumi)
- ✅ **Setup Validation**: Checks everything is configured before running
- ✅ **Better Errors**: Clear, actionable error messages (no more stack traces!)
- ✅ **Progress Feedback**: See what's happening in real-time
- ✅ **Test Mode**: Validate your setup works
- ✅ **Updated Libraries**: Fixed API compatibility issues from v1

---

## 🚀 Quick Start

### 1. Install Python 3.8+

Check your version:
```bash
python3 --version
```

If you need to install Python: [python.org/downloads](https://www.python.org/downloads/)

### 2. Install FinCat

```bash
cd "/Users/nathanhivishnevski/Desktop/AutoMates - ClaudeCode/PM/Branch (Version) Management/FinCat/v2"

# Create virtual environment
python3 -m venv venv

# Activate (Mac/Linux)
source venv/bin/activate

# Activate (Windows)
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Get API Key

1. Go to: [console.anthropic.com](https://console.anthropic.com/)
2. Sign up / Log in
3. Create API key
4. Copy the key (starts with `sk-ant-`)

### 4. Configure FinCat

```bash
# Copy example config
cp config/.env.example config/.env

# Edit and add your API key
nano config/.env  # or use any text editor
```

In `config/.env`, set:
```
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

### 5. Validate Setup

```bash
python -m fincat.main --setup
```

You should see:
```
✅ Python 3.8+
✅ Config file valid
✅ .env file exists with API key
✅ All folders created/validated
✅ API key valid (test call successful)

✅ All checks passed! FinCat is ready to use.
```

### 6. Test with Sample File

```bash
python -m fincat.main --test
```

### 7. Start Using

```bash
# Watch mode (continuous)
python -m fincat.main

# Manual mode (process once)
python -m fincat.main --manual
```

---

## 📁 How It Works

1. **Drop File**: Put Hebrew credit card .xls/.xlsx file in `input/` folder
2. **Auto-Process**: FinCat detects file, parses transactions
3. **AI Categorize**: Claude categorizes each expense
4. **Update Master**: Appends to `data/מעקב_חיובים.xlsx`
5. **Archive**: Moves processed file to `processed/` folder

---

## 🗂️ Folder Structure

```
v2/
├── input/                  # Drop credit card files here
├── processed/              # Processed files archived here
├── data/
│   ├── מעקב_חיובים.xlsx   # Master tracking file
│   └── קטגוריות.xlsx       # Categories (auto-created)
├── logs/
│   └── fincat.log          # Application logs
├── config/
│   ├── config.yaml         # Settings
│   └── .env                # Your API key (SECRET!)
└── fincat/                 # Source code
```

---

## 🛠️ Commands

| Command | Description |
|---------|-------------|
| `python -m fincat.main` | Watch mode (runs continuously) |
| `python -m fincat.main --manual` | Process all files once, then exit |
| `python -m fincat.main --setup` | Validate setup and configuration |
| `python -m fincat.main --test` | Test with sample file |
| `python -m fincat.main --verbose` | Show detailed debug logs |

---

## 🏦 Supported Banks

FinCat v2 has been tested with:
- ✅ American Express (Amex)
- ✅ Cal (כאל)
- ✅ Leumi (לאומי)
- ✅ Generic Israeli credit card format

**Different bank format?** FinCat's smart header detection should handle it. If not, open an issue!

---

## ❓ Troubleshooting

### "❌ API key invalid"
**Fix:**
1. Get new key from: [console.anthropic.com](https://console.anthropic.com/)
2. Update `config/.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-new-key
   ```
3. Run: `python -m fincat.main --setup`

### "❌ .env file not found"
**Fix:**
```bash
cp config/.env.example config/.env
nano config/.env  # Add your API key
```

### "Cannot write to file"
**Fix:** Close the Excel file `data/מעקב_חיובים.xlsx` and try again

### "No transactions found"
**Fix:** Your file format might be different. Enable verbose logging:
```bash
python -m fincat.main --verbose
```
Check `logs/fincat.log` for details. The parser logs which rows it's finding.

### "ModuleNotFoundError"
**Fix:**
```bash
source venv/bin/activate  # Activate virtual environment first
pip install -r requirements.txt
```

### Still stuck?
1. Check `logs/fincat.log` for details
2. Run with `--verbose` flag
3. Open an issue on GitHub with the log file

---

## 🔒 Security

- **API Key**: Never commit `config/.env` to git (it's in `.gitignore`)
- **Data**: All processing happens locally, only business names sent to Claude
- **Logs**: No sensitive data (API keys, amounts) logged

---

## 📊 Cost

- **API Costs**: ~$0.0006 per file (50 transactions)
- **Estimated**: < $0.10/month for typical use
- Uses Claude Haiku (most cost-efficient model)

---

## 🚀 Upgrading from v1

```bash
# Backup your data
cp -r v1/data v1/data.backup

# Install v2
cd v2
pip install -r requirements.txt --upgrade

# Copy your API key
cp ../v1/config/.env config/.env

# Validate
python -m fincat.main --setup

# Continue using (same commands)
python -m fincat.main
```

**Note:** v2 uses the same master file format, so your existing data works as-is!

---

## 📝 License

MIT License

---

## 🤝 Contributing

Found a bug? Have a feature request? Open an issue!

---

**Made with ❤️  using Claude AI**
