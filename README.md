# Local LLM Policy Gap Analysis and Improvement Module

A fully offline, privacy-focused system for analyzing organizational cybersecurity policies against NIST Cybersecurity Framework standards using a lightweight Large Language Model running entirely on your local machine.

## 🎯 Project Overview

This system helps organizations improve their cybersecurity policies by:
- **Identifying gaps** in existing policies compared to NIST CSF standards
- **Generating revised policies** that address identified weaknesses
- **Creating implementation roadmaps** with phased improvement plans
- **Operating completely offline** with no cloud services or external APIs

### Supported Policy Types
- Information Security Management System (ISMS)
- Data Privacy and Security
- Patch Management
- Risk Management

## ✨ Key Features

- ✅ **100% Offline Operation** - No internet required after initial setup
- ✅ **Privacy-First** - All data stays on your local machine
- ✅ **Lightweight LLM** - Runs on standard hardware (8GB RAM minimum)
- ✅ **NIST CSF Aligned** - Based on CIS MS-ISAC NIST CSF Policy Template Guide (2024)
- ✅ **Multiple Formats** - Supports TXT, PDF, and DOCX for policies and reference frameworks
- ✅ **Professional PDF Output** - Formatted reports with markdown styling
- ✅ **Comprehensive Reports** - Gap analysis, revised policies, and roadmaps
- ✅ **Batch Processing** - Analyze multiple policies at once

## 📋 System Requirements

### Hardware
- **CPU:** Modern multi-core processor (Intel i5/AMD Ryzen 5 or better)
- **RAM:** 8GB minimum, 16GB recommended
- **Storage:** 10GB free space (for model and data)
- **OS:** Windows 10/11, Linux, or macOS

### Software
- **Python:** 3.8 or higher
- **Ollama:** Local LLM runtime (free, open-source)
- **LLM Model:** Gemma3 (latest)

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download the project
cd "Local LLM"

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Install Ollama

Download and install Ollama from: https://ollama.ai/download

### 3. Download LLM Model

```bash
ollama pull gemma3:latest
```

**Note:** This requires internet connection (one-time only). After download, the system operates completely offline.

### 4. Verify Setup

```bash
python test_system.py --verify-offline
```

### 5. Run Sample Analysis

```bash
python src/main.py --policy data/test_policies/isms_policy.txt
```

## 📖 Usage

### Analyze Single Policy

```bash
python src/main.py --policy path/to/policy.txt
```

### Analyze Multiple Policies (Batch)

```bash
python src/main.py --batch data/test_policies/
```

### Specify Output Directory

```bash
python src/main.py --policy policy.txt --output results/
```

### Supported File Formats

**Policy Documents (Input):**
- **Text files:** `.txt`
- **PDF documents:** `.pdf`
- **Word documents:** `.docx`

**Reference Frameworks (NIST Standards):**
- **Text files:** `.txt`
- **PDF documents:** `.pdf`

## 📊 Output Reports

The system generates 5 comprehensive reports for each policy in **both TXT and PDF formats**:

1. **Gap Analysis Report** - Detailed list of missing/weak provisions with NIST references
2. **Revised Policy Document** - Improved policy addressing all identified gaps
3. **Implementation Roadmap** - Phased plan (0-3, 3-6, 6-12 months) with milestones
4. **Executive Summary** - High-level overview for leadership
5. **Comprehensive Report** - All above combined in one document

### Sample Output Structure

```
output/
├── isms_policy_20240115_143022_gap_analysis.txt
├── isms_policy_20240115_143022_gap_analysis.pdf          ← Professional PDF
├── isms_policy_20240115_143022_revised_policy.txt
├── isms_policy_20240115_143022_revised_policy.pdf        ← Professional PDF
├── isms_policy_20240115_143022_roadmap.txt
├── isms_policy_20240115_143022_roadmap.pdf               ← Professional PDF
├── isms_policy_20240115_143022_executive_summary.txt
├── isms_policy_20240115_143022_executive_summary.pdf     ← Professional PDF
├── isms_policy_20240115_143022_comprehensive_report.txt
└── isms_policy_20240115_143022_comprehensive_report.pdf  ← Professional PDF
```

## ⏱️ Processing Time

Typical processing time per policy (on standard hardware):
- Gap Analysis: 1-2 minutes
- Policy Revision: 2-3 minutes
- Roadmap Generation: 1-2 minutes
- Executive Summary: 30-60 seconds

**Total: ~5-8 minutes per policy**

## 🔒 Privacy & Security

- **No Cloud Services** - Everything runs locally
- **No External APIs** - Zero network calls during operation
- **No Data Collection** - Your policies never leave your machine
- **Offline Operation** - Works without internet connection
- **Open Source** - Transparent, auditable code

## 📚 Documentation

### Setup & Usage
- **[INSTALLATION.md](docs/INSTALLATION.md)** - Detailed setup instructions
- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide with examples
- **[VALIDATION_CHECKLIST.md](VALIDATION_CHECKLIST.md)** - Testing and validation

### Technical Documentation
- **[TECHNICAL_GUIDE.md](docs/TECHNICAL_GUIDE.md)** - Architecture and technical details
- **[USER_GUIDE.md](docs/USER_GUIDE.md)** - Comprehensive user guide

### PDF Output Feature
- **[PDF_GENERATION_GUIDE.md](docs/PDF_GENERATION_GUIDE.md)** - Complete PDF output guide
- **[QUICKSTART_PDF.md](docs/QUICKSTART_PDF.md)** - Quick PDF feature reference
- **[BEFORE_AFTER_COMPARISON.md](docs/BEFORE_AFTER_COMPARISON.md)** - Visual comparison
- **[PDF_ENHANCEMENT_SUMMARY.md](docs/PDF_ENHANCEMENT_SUMMARY.md)** - Technical implementation
- **[IMPLEMENTATION_COMPLETE.md](docs/IMPLEMENTATION_COMPLETE.md)** - Full implementation summary

## 🧪 Testing

### Run Full Test Suite

```bash
python test_system.py --test-all
```

### Test Specific Policy

```bash
python test_system.py --test-policy data/test_policies/isms_policy.txt
```

### Verify Offline Operation

```bash
python test_system.py --verify-offline
```

## 🛠️ Troubleshooting

### "ollama: command not found"
- Install Ollama from https://ollama.ai/download
- Restart terminal after installation

### "Model not found"
- Download model: `ollama pull gemma3:latest`
- Verify: `ollama list`

### Slow Performance
- Ensure sufficient RAM (16GB recommended)
- Close other applications
- Consider using a smaller model
- First run may be slower (model loading)

### "LLM execution failed"
- Verify Ollama is running: `ollama --version`
- Check model is downloaded: `ollama list`
- Try manual test: `ollama run gemma3:latest`

## 📁 Project Structure

```
Local LLM/
├── src/                        # Source code
│   ├── main.py                 # Main entry point
│   ├── gap_analyzer.py         # Gap identification
│   ├── policy_reviser.py       # Policy revision
│   ├── roadmap_generator.py    # Roadmap creation
│   ├── pdf_generator.py        # PDF output generation
│   └── utils.py                # Utilities
├── data/
│   ├── reference/              # NIST framework (TXT/PDF)
│   └── test_policies/          # Sample policies (TXT/PDF/DOCX)
├── output/                     # Generated reports (TXT + PDF)
├── docs/                       # Documentation
├── requirements.txt            # Python dependencies
├── convert_to_pdf.py           # Convert existing reports to PDF
└── test_system.py             # Test suite
```

## 🎓 How It Works

1. **Load Policy** - System reads your policy document (TXT/PDF/DOCX)
2. **Load NIST Standards** - Loads NIST CSF reference framework
3. **Gap Analysis** - LLM compares policy against NIST standards
4. **Policy Revision** - LLM generates improved policy version
5. **Roadmap Creation** - LLM creates phased implementation plan
6. **Report Generation** - Outputs comprehensive reports

All processing happens locally using Ollama and a lightweight LLM model.

## 🔄 NIST Framework Coverage

Based on **CIS MS-ISAC NIST Cybersecurity Framework Policy Template Guide (2024)**

### Core Functions
- **Identify (ID)** - Asset management, risk assessment, governance
- **Protect (PR)** - Access control, data security, training
- **Detect (DE)** - Monitoring, anomaly detection
- **Respond (RS)** - Response planning, communications, mitigation
- **Recover (RC)** - Recovery planning, improvements

## 🤝 Contributing

This is an academic/research project. Suggestions for improvements:
- Support for additional frameworks (ISO 27001, GDPR, SOC 2)
- Multi-language policy support
- Enhanced visualization and reporting
- Performance optimizations
- Additional LLM model support

## ⚠️ Limitations

- **Model Accuracy** - LLM outputs may require human review
- **Processing Time** - Analysis takes 5-8 minutes per policy
- **Hardware Requirements** - Needs 8GB+ RAM for optimal performance
- **Format Support** - Complex PDF layouts may not parse perfectly
- **Language** - Currently optimized for English policies

## 📄 License

This project is provided for educational and research purposes.

## 🙏 Acknowledgments

- **NIST Cybersecurity Framework** - Framework standards
- **CIS MS-ISAC** - Policy template guide (2024)
- **Ollama** - Local LLM runtime
- **Google** - Gemma3 LLM model

## 📞 Support

For issues or questions:
1. Check [TROUBLESHOOTING](QUICKSTART.md#troubleshooting) section
2. Review [TECHNICAL_GUIDE.md](docs/TECHNICAL_GUIDE.md)
3. Verify system setup: `python test_system.py --verify-offline`

---

**Version:** 1.1  
**Last Updated:** February 2026  
**Framework:** NIST CSF (CIS MS-ISAC 2024)  
**New Features:** PDF Output Generation, Multi-Format Reference Support
