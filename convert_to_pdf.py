"""Test script to convert existing text reports to PDF format."""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pdf_generator import create_pdf_report

def convert_existing_reports():
    """Convert all existing text reports in output folder to PDF."""
    
    output_dir = Path('output')
    txt_files = list(output_dir.glob('*.txt'))
    
    if not txt_files:
        print("No text reports found in output folder.")
        return
    
    print(f"Found {len(txt_files)} text reports to convert\\n")
    
    for txt_file in txt_files:
        try:
            # Read content
            with open(txt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Generate PDF
            pdf_file = txt_file.with_suffix('.pdf')
            
            # Determine title from filename
            if 'gap_analysis' in txt_file.name:
                title = "Gap Analysis Report"
            elif 'revised_policy' in txt_file.name:
                title = "Revised Policy Document"
            elif 'roadmap' in txt_file.name:
                title = "Implementation Roadmap"
            elif 'executive_summary' in txt_file.name:
                title = "Executive Summary"
            elif 'comprehensive' in txt_file.name:
                title = "Comprehensive Policy Analysis"
            else:
                title = "Policy Analysis Report"
            
            create_pdf_report(content, str(pdf_file), title)
            print(f"OK Generated: {pdf_file.name}")
            
        except Exception as e:
            print(f"FAILED to convert {txt_file.name}: {e}")
    
    print(f"\\nPDF conversion complete!")

if __name__ == '__main__':
    convert_existing_reports()
