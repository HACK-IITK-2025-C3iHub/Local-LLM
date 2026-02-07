# Installation Guide

## Prerequisites

- Python 3.8 or higher
- Windows 10/11, Linux, or macOS
- 8GB RAM minimum (16GB recommended)

## Setup Steps

### 1. Install Python Packages

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install ollama PyPDF2 python-docx reportlab
```

### 2. Install Ollama

**Windows:**
```bash
# Download and run installer from:
https://ollama.ai/download
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**macOS:**
```bash
brew install ollama
```

### 3. Download LLM Model

```bash
ollama pull gemma3:4b
```

### 4. Verify Installation

```bash
# Check Ollama
ollama --version

# Check model
ollama list

# Test system
python test_system.py --verify-offline
```

## Quick Test

```bash
python src/main.py --policy data/test_policies/isms_policy.txt
```

## Troubleshooting

**Ollama not found:**
```bash
# Restart terminal after Ollama installation
```

**Model not found:**
```bash
ollama pull gemma3:4b
```

**Python packages error:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

**Setup complete!** System is ready for offline operation.
