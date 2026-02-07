"""Demo script showing support for TXT, PDF, and DOCX policy formats."""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils import read_policy_document

def demo_format_support():
    """Demonstrate reading policies in different formats."""
    
    print("="*60)
    print("POLICY FORMAT SUPPORT DEMONSTRATION")
    print("="*60)
    print("\nThe system supports the following formats:")
    print("  - .txt  (Plain text)")
    print("  - .pdf  (PDF documents)")
    print("  - .docx (Word documents)")
    print("\n" + "="*60 + "\n")
    
    # Test with existing TXT file
    test_policies_dir = Path('data/test_policies')
    
    # Find all policy files
    txt_files = list(test_policies_dir.glob('*.txt'))
    pdf_files = list(test_policies_dir.glob('*.pdf'))
    docx_files = list(test_policies_dir.glob('*.docx'))
    
    print(f"Found in test_policies folder:")
    print(f"  - TXT files:  {len(txt_files)}")
    print(f"  - PDF files:  {len(pdf_files)}")
    print(f"  - DOCX files: {len(docx_files)}")
    print()
    
    # Test reading a TXT file
    if txt_files:
        print(f"Testing TXT format: {txt_files[0].name}")
        try:
            content = read_policy_document(str(txt_files[0]))
            print(f"  ✓ Successfully read {len(content)} characters")
            print(f"  Preview: {content[:100]}...")
        except Exception as e:
            print(f"  ✗ Error: {e}")
        print()
    
    # Test reading a PDF file (if exists)
    if pdf_files:
        print(f"Testing PDF format: {pdf_files[0].name}")
        try:
            content = read_policy_document(str(pdf_files[0]))
            print(f"  ✓ Successfully read {len(content)} characters")
            print(f"  Preview: {content[:100]}...")
        except Exception as e:
            print(f"  ✗ Error: {e}")
        print()
    
    # Test reading a DOCX file (if exists)
    if docx_files:
        print(f"Testing DOCX format: {docx_files[0].name}")
        try:
            content = read_policy_document(str(docx_files[0]))
            print(f"  ✓ Successfully read {len(content)} characters")
            print(f"  Preview: {content[:100]}...")
        except Exception as e:
            print(f"  ✗ Error: {e}")
        print()
    
    print("="*60)
    print("USAGE EXAMPLES")
    print("="*60)
    print("\n1. Analyze TXT policy:")
    print("   python src/main.py --policy data/test_policies/isms_policy.txt")
    print("\n2. Analyze PDF policy:")
    print("   python src/main.py --policy data/test_policies/policy.pdf")
    print("\n3. Analyze DOCX policy:")
    print("   python src/main.py --policy data/test_policies/policy.docx")
    print("\n4. Batch analyze all formats:")
    print("   python src/main.py --batch data/test_policies/")
    print("\n" + "="*60)
    print("\nAll formats are automatically detected by file extension!")
    print("="*60 + "\n")

if __name__ == '__main__':
    demo_format_support()
