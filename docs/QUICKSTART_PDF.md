# Quick Start: PDF Output Feature

## Installation

```bash
# Install PDF generation library
pip install reportlab

# Or install all dependencies
pip install -r requirements.txt
```

## Usage

### Option 1: Run New Analysis (Automatic PDF Generation)

```bash
python src/main.py --policy data/test_policies/isms_policy.txt
```

**Output:** Both .txt and .pdf files generated automatically

### Option 2: Convert Existing Reports

```bash
python convert_to_pdf.py
```

**Output:** PDF versions of all existing .txt reports in output/ folder

## What You Get

For each policy analysis, you receive **10 files** (5 TXT + 5 PDF):

1. **Gap Analysis** - Identifies policy weaknesses
   - `*_gap_analysis.txt`
   - `*_gap_analysis.pdf` ← NEW

2. **Revised Policy** - Improved policy document
   - `*_revised_policy.txt`
   - `*_revised_policy.pdf` ← NEW

3. **Implementation Roadmap** - Phased improvement plan
   - `*_roadmap.txt`
   - `*_roadmap.pdf` ← NEW

4. **Executive Summary** - High-level overview
   - `*_executive_summary.txt`
   - `*_executive_summary.pdf` ← NEW

5. **Comprehensive Report** - All reports combined
   - `*_comprehensive_report.txt`
   - `*_comprehensive_report.pdf` ← NEW

## PDF Features

- ✅ Professional formatting
- ✅ Markdown support (headings, bold, bullets)
- ✅ Print-ready layout
- ✅ Easy to share and archive

## Example

```bash
# Analyze ISMS policy
python src/main.py --policy data/test_policies/isms_policy.txt

# Check output folder
ls output/

# You'll see:
# isms_policy_20260207_162145_gap_analysis.txt
# isms_policy_20260207_162145_gap_analysis.pdf          ← Formatted PDF
# isms_policy_20260207_162145_revised_policy.txt
# isms_policy_20260207_162145_revised_policy.pdf        ← Formatted PDF
# ... and so on
```

## Troubleshooting

**Problem:** "reportlab not found"  
**Solution:** `pip install reportlab`

**Problem:** PDF generation failed  
**Solution:** Text reports are still available. Check console for error details.

## More Information

- Full guide: [PDF_GENERATION_GUIDE.md](PDF_GENERATION_GUIDE.md)
- Implementation details: [PDF_ENHANCEMENT_SUMMARY.md](PDF_ENHANCEMENT_SUMMARY.md)

---

**That's it!** Your reports now come in professional PDF format automatically.
