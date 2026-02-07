# Quick Start Guide

## Prerequisites Check

Before running the system, ensure you have completed the installation steps from `docs/INSTALLATION.md`.

## Step 1: Verify System Setup

```bash
python test_system.py --verify-offline
```

This will check:
- ✓ Ollama is installed
- ✓ LLM model is downloaded
- ✓ No external API calls in code
- ✓ Local reference data is available

## Step 2: Test Single Policy

Test the system with one policy:

```bash
python src/main.py --policy data/test_policies/isms_policy.txt
```

Expected output files in `output/` directory:
- `isms_policy_TIMESTAMP_gap_analysis.txt`
- `isms_policy_TIMESTAMP_revised_policy.txt`
- `isms_policy_TIMESTAMP_roadmap.txt`
- `isms_policy_TIMESTAMP_executive_summary.txt`
- `isms_policy_TIMESTAMP_comprehensive_report.txt`

## Step 3: Analyze All Test Policies

Run batch analysis on all dummy policies:

```bash
python src/main.py --batch data/test_policies/
```

This will analyze all 4 policies:
1. ISMS Policy
2. Data Privacy and Security Policy
3. Patch Management Policy
4. Risk Management Policy

## Step 4: Run Full Test Suite

```bash
python test_system.py --test-all
```

This validates the system against all test policies and generates reports.

## Expected Processing Time

Per policy (on typical hardware):
- Gap Analysis: 1-2 minutes
- Policy Revision: 2-3 minutes
- Roadmap Generation: 1-2 minutes
- Executive Summary: 30-60 seconds

**Total per policy: ~5-8 minutes**

## Analyzing Your Own Policies

### Text File (.txt)
```bash
python src/main.py --policy path/to/your/policy.txt
```

### PDF File (.pdf)
```bash
python src/main.py --policy path/to/your/policy.pdf
```

### Word Document (.docx)
```bash
python src/main.py --policy path/to/your/policy.docx
```

## Troubleshooting

### Error: "ollama: command not found"
- Install Ollama from https://ollama.ai/download
- Restart terminal after installation

### Error: "Model not found"
- Download model: `ollama pull gemma3:latest`
- Verify: `ollama list`

### Error: "LLM execution failed"
- Ensure Ollama service is running
- Check model is downloaded: `ollama list`
- Try running: `ollama run gemma3:latest` manually

### Slow Performance
- First run downloads model (one-time, requires internet)
- Subsequent runs are fully offline
- Consider using a smaller model for faster processing
- Ensure sufficient RAM (8GB minimum, 16GB recommended)

## Offline Operation

After initial setup:
1. Model is cached locally in Ollama
2. All reference data is in `data/reference/`
3. No internet connection required
4. System operates completely offline

To verify offline operation:
```bash
# Disconnect from internet, then run:
python test_system.py --verify-offline
```

## Output Files Explained

1. **Gap Analysis** - Detailed list of missing/weak provisions
2. **Revised Policy** - Improved policy addressing all gaps
3. **Roadmap** - Phased implementation plan (0-12 months)
4. **Executive Summary** - High-level overview for leadership
5. **Comprehensive Report** - All above combined in one document

## Next Steps

1. Review generated reports in `output/` directory
2. Compare gap analysis with `data/test_policies/GAPS_DOCUMENTATION.md`
3. Validate roadmap alignment with NIST framework
4. Use revised policies as templates for your organization
