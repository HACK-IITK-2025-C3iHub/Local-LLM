"""Demo: Multi-Format Support for Policies and Reference Frameworks"""

import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils import read_policy_document

print("="*70)
print("MULTI-FORMAT SUPPORT DEMONSTRATION")
print("="*70)
print("\n✓ The system now supports TXT, PDF, and DOCX formats for:")
print("  1. Policy documents (input)")
print("  2. Reference frameworks (NIST standards)")
print()

# Check test policies
print("="*70)
print("TEST POLICIES (Input)")
print("="*70)

test_dir = Path('data/test_policies')
txt_files = list(test_dir.glob('*.txt'))
pdf_files = list(test_dir.glob('*.pdf'))
docx_files = list(test_dir.glob('*.docx'))

print(f"\nFound in data/test_policies/:")
print(f"  • TXT files:  {len(txt_files)}")
for f in txt_files:
    print(f"    - {f.name}")
print(f"  • PDF files:  {len(pdf_files)}")
for f in pdf_files:
    print(f"    - {f.name}")
print(f"  • DOCX files: {len(docx_files)}")
for f in docx_files:
    print(f"    - {f.name}")

# Check reference frameworks
print("\n" + "="*70)
print("REFERENCE FRAMEWORKS (NIST Standards)")
print("="*70)

ref_dir = Path('data/reference')
ref_txt = list(ref_dir.glob('*.txt'))
ref_pdf = list(ref_dir.glob('*.pdf'))

print(f"\nFound in data/reference/:")
print(f"  • TXT files:  {len(ref_txt)}")
for f in ref_txt:
    print(f"    - {f.name}")
print(f"  • PDF files:  {len(ref_pdf)}")
for f in ref_pdf:
    print(f"    - {f.name}")

# Test reading
print("\n" + "="*70)
print("FORMAT VALIDATION TEST")
print("="*70)

# Test TXT policy
if txt_files:
    print(f"\n✓ Testing TXT policy: {txt_files[0].name}")
    try:
        content = read_policy_document(str(txt_files[0]))
        print(f"  Success! Read {len(content)} characters")
    except Exception as e:
        print(f"  Error: {e}")

# Test PDF reference
if ref_pdf:
    print(f"\n✓ Testing PDF reference: {ref_pdf[0].name}")
    try:
        content = read_policy_document(str(ref_pdf[0]))
        print(f"  Success! Read {len(content)} characters")
    except Exception as e:
        print(f"  Error: {e}")

# Usage examples
print("\n" + "="*70)
print("USAGE EXAMPLES")
print("="*70)

print("\n1. Analyze TXT policy with TXT reference:")
print("   python src/main.py --policy data/test_policies/isms_policy.txt")

print("\n2. Analyze PDF policy (if available):")
print("   python src/main.py --policy data/test_policies/policy.pdf")

print("\n3. Analyze DOCX policy (if available):")
print("   python src/main.py --policy data/test_policies/policy.docx")

print("\n4. Batch analyze all formats:")
print("   python src/main.py --batch data/test_policies/")

print("\n5. System auto-detects reference format:")
print("   - Looks in data/reference/ folder")
print("   - Uses TXT if available, otherwise PDF")
print("   - No manual configuration needed!")

print("\n" + "="*70)
print("KEY FEATURES")
print("="*70)
print("\n✓ Automatic format detection by file extension")
print("✓ Supports .txt, .pdf, .docx for policies")
print("✓ Supports .txt, .pdf for reference frameworks")
print("✓ No manual configuration required")
print("✓ Batch processing works with mixed formats")
print("✓ File size validation (max 50MB)")
print("✓ Error handling for corrupted files")

print("\n" + "="*70)
print("HOW IT WORKS")
print("="*70)
print("\n1. Policy Input:")
print("   - Place your policy file in data/test_policies/")
print("   - Use any format: .txt, .pdf, or .docx")
print("   - Run analysis with --policy flag")

print("\n2. Reference Framework:")
print("   - Place NIST framework in data/reference/")
print("   - Use .txt or .pdf format")
print("   - System auto-detects and loads it")

print("\n3. Output:")
print("   - Always generates both TXT and PDF reports")
print("   - Saved in output/ folder")
print("   - Professional formatting applied")

print("\n" + "="*70)
print()
