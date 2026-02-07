# User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Basic Usage](#basic-usage)
3. [Advanced Features](#advanced-features)
4. [Understanding Reports](#understanding-reports)
5. [Best Practices](#best-practices)
6. [FAQ](#faq)

## Getting Started

### First Time Setup

1. **Complete Installation**
   - Follow steps in [INSTALLATION.md](INSTALLATION.md)
   - Verify setup: `python test_system.py --verify-offline`

2. **Test with Sample Policy**
   ```bash
   python src/main.py --policy data/test_policies/isms_policy.txt
   ```

3. **Review Output**
   - Check `output/` directory for generated reports
   - Review each report type to understand format

## Basic Usage

### Analyzing a Single Policy

**Command:**
```bash
python src/main.py --policy path/to/your/policy.txt
```

**Example:**
```bash
python src/main.py --policy "C:\Policies\InfoSec_Policy.txt"
```

**What Happens:**
1. System loads your policy document
2. Loads NIST framework standards
3. Analyzes gaps (1-2 minutes)
4. Generates revised policy (2-3 minutes)
5. Creates implementation roadmap (1-2 minutes)
6. Produces executive summary (30-60 seconds)
7. Saves 5 reports to `output/` directory

### Analyzing Multiple Policies

**Command:**
```bash
python src/main.py --batch path/to/policies/folder/
```

**Example:**
```bash
python src/main.py --batch data/test_policies/
```

**What Happens:**
- System finds all TXT, PDF, and DOCX files in folder
- Analyzes each policy sequentially
- Generates separate reports for each policy
- Progress shown for each policy

### Specifying Output Location

**Command:**
```bash
python src/main.py --policy policy.txt --output custom_folder/
```

**Example:**
```bash
python src/main.py --policy isms.txt --output results/january_2024/
```

## Advanced Features

### Working with Different File Formats

**Text Files (.txt):**
```bash
python src/main.py --policy policy.txt
```
- Fastest processing
- Recommended format
- Best for plain text policies

**PDF Files (.pdf):**
```bash
python src/main.py --policy policy.pdf
```
- Automatically extracts text
- Works with most PDF formats
- Complex layouts may need manual review

**Word Documents (.docx):**
```bash
python src/main.py --policy policy.docx
```
- Extracts text from Word documents
- Preserves paragraph structure
- Tables may need special handling

### Batch Processing Tips

1. **Organize Policies by Type**
   ```
   policies/
   ├── isms/
   ├── privacy/
   ├── patch_mgmt/
   └── risk_mgmt/
   ```

2. **Process by Category**
   ```bash
   python src/main.py --batch policies/isms/ --output results/isms/
   python src/main.py --batch policies/privacy/ --output results/privacy/
   ```

3. **Review Results Systematically**
   - Start with executive summaries
   - Review gap analyses for priorities
   - Use roadmaps for planning

## Understanding Reports

### 1. Gap Analysis Report

**Purpose:** Identifies all weaknesses and missing elements

**Structure:**
- **Critical Gaps** - High priority, immediate attention needed
- **Significant Gaps** - Medium priority, important improvements
- **Minor Gaps** - Low priority, optimization opportunities
- **Summary** - Overall assessment

**How to Use:**
1. Start with Critical Gaps - these are security risks
2. Review NIST references to understand requirements
3. Prioritize based on your organization's risk profile
4. Use as input for security planning

**Example Gap:**
```
Missing Multi-Factor Authentication (MFA) requirement
NIST Reference: PR.AC-7 (Identity Management and Access Control)
Impact: High - Increases risk of unauthorized access
Recommendation: Implement MFA for all privileged accounts
```

### 2. Revised Policy Document

**Purpose:** Improved policy addressing all identified gaps

**Structure:**
- Maintains original policy organization
- Adds missing sections and provisions
- Enhances weak areas with specific requirements
- Includes clear roles and responsibilities

**How to Use:**
1. Compare with original policy (side-by-side)
2. Review new sections and provisions
3. Adapt language to your organization's style
4. Have legal/compliance review changes
5. Use as template for policy update

**Key Improvements:**
- Specific, actionable requirements
- Clear accountability assignments
- Measurable success criteria
- Compliance references

### 3. Implementation Roadmap

**Purpose:** Phased plan for implementing improvements

**Structure:**
- **Phase 1 (0-3 months)** - Critical gaps, immediate actions
- **Phase 2 (3-6 months)** - Significant improvements
- **Phase 3 (6-12 months)** - Long-term enhancements
- **NIST Alignment** - Maps to framework functions
- **Resources** - Personnel, technology, budget needs
- **Milestones** - Key checkpoints and deliverables
- **Metrics** - Success measurement criteria

**How to Use:**
1. Review with IT and security teams
2. Assess resource availability
3. Adjust timelines based on capacity
4. Integrate with existing projects
5. Track progress against milestones

**Example Action:**
```
Phase 1 Action: Implement MFA for Privileged Accounts
- NIST Function: Protect (PR.AC)
- Timeline: Month 1-2
- Resources: MFA solution, 40 hours implementation
- Success Criteria: 100% privileged accounts using MFA
- Dependencies: User training, helpdesk preparation
```

### 4. Executive Summary

**Purpose:** High-level overview for leadership

**Structure:**
- Current state assessment
- Key findings (top 3-5 issues)
- Risk exposure summary
- Recommended actions
- Investment requirements
- Expected outcomes
- Implementation timeline

**How to Use:**
1. Present to senior management
2. Use for budget justification
3. Communicate security posture
4. Gain executive buy-in
5. Align with business objectives

**Audience:** CIO, CISO, Board, Executive Team

### 5. Comprehensive Report

**Purpose:** All-in-one document with complete analysis

**Contains:**
- Executive summary
- Detailed gap analysis
- Revised policy
- Implementation roadmap

**How to Use:**
- Archive for compliance records
- Share with audit teams
- Reference document for implementation
- Training material for security team

## Best Practices

### Before Analysis

1. **Prepare Policy Documents**
   - Convert to TXT format if possible (fastest)
   - Ensure text is readable (not scanned images)
   - Remove unnecessary formatting
   - Verify file is complete

2. **Understand Your Context**
   - Know your organization's risk appetite
   - Identify regulatory requirements
   - Consider existing security controls
   - Assess resource constraints

3. **Set Expectations**
   - Analysis takes 5-8 minutes per policy
   - LLM output requires human review
   - Results are recommendations, not mandates
   - Customization needed for your organization

### During Analysis

1. **Monitor Progress**
   - Watch console output for errors
   - Ensure sufficient system resources
   - Don't interrupt the process
   - Note any warnings or issues

2. **System Performance**
   - Close unnecessary applications
   - Ensure adequate RAM available
   - First run may be slower (model loading)
   - Subsequent runs are faster

### After Analysis

1. **Review Reports Systematically**
   - Start with executive summary
   - Deep dive into gap analysis
   - Compare revised policy with original
   - Assess roadmap feasibility

2. **Validate Findings**
   - Cross-reference with NIST framework
   - Verify gaps against current controls
   - Consult with security team
   - Consider organizational context

3. **Customize Recommendations**
   - Adapt to your organization's size
   - Align with existing processes
   - Consider budget constraints
   - Prioritize based on risk

4. **Plan Implementation**
   - Use roadmap as starting point
   - Adjust timelines realistically
   - Assign clear ownership
   - Track progress regularly

## FAQ

### General Questions

**Q: How accurate is the gap analysis?**
A: The LLM provides comprehensive analysis based on NIST standards, but human review is essential. Expect 80-90% accuracy with some false positives/negatives.

**Q: Can I use this for compliance audits?**
A: The reports provide valuable input for compliance, but should be reviewed by qualified auditors. This is a tool to assist, not replace, professional assessment.

**Q: Does this work offline?**
A: Yes, completely offline after initial setup. No internet required during analysis.

**Q: How long does analysis take?**
A: 5-8 minutes per policy on standard hardware (8GB RAM, modern CPU).

### Technical Questions

**Q: Which LLM model should I use?**
A: Mistral-7B-Instruct (recommended) or Llama-3-8B-Instruct. Both are lightweight and effective.

**Q: Can I use a different LLM framework?**
A: The code uses Ollama. You can modify `gap_analyzer.py` to use other frameworks (llama.cpp, GPT4All).

**Q: What if my PDF doesn't parse correctly?**
A: Convert to TXT format manually or use OCR tools for scanned documents.

**Q: Can I customize the NIST framework reference?**
A: Yes, edit `data/reference/nist_framework.txt` to add organization-specific requirements.

### Usage Questions

**Q: Can I analyze policies in other languages?**
A: The system is optimized for English. Other languages may work but with reduced accuracy.

**Q: How do I analyze a very long policy (50+ pages)?**
A: The system handles long documents, but consider splitting into logical sections for better analysis.

**Q: Can I compare two versions of the same policy?**
A: Not directly. Analyze each version separately and compare the gap analyses.

**Q: What if I disagree with a finding?**
A: LLM recommendations are suggestions. Use professional judgment to accept/reject findings based on your context.

### Troubleshooting

**Q: Analysis is very slow**
A: Ensure 16GB RAM, close other apps, check CPU usage, consider smaller model.

**Q: Getting "Model not found" error**
A: Run `ollama pull mistral:7b-instruct` to download the model.

**Q: Output seems incomplete**
A: Check console for errors, verify model is working (`ollama run mistral:7b-instruct`), ensure sufficient disk space.

**Q: Can't find output files**
A: Check `output/` directory, verify write permissions, check console for save errors.

## Getting Help

1. **Check Documentation**
   - README.md - Overview and quick start
   - INSTALLATION.md - Setup instructions
   - TECHNICAL_GUIDE.md - Architecture details
   - QUICKSTART.md - Examples and troubleshooting

2. **Run Diagnostics**
   ```bash
   python test_system.py --verify-offline
   ```

3. **Test with Sample Policy**
   ```bash
   python src/main.py --policy data/test_policies/isms_policy.txt
   ```

4. **Review Validation Checklist**
   - See VALIDATION_CHECKLIST.md for comprehensive testing

---

**Need more help?** Review the technical documentation or check system logs for detailed error messages.
