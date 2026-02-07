"""PDF generation module with markdown formatting support."""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.colors import HexColor
from datetime import datetime
import re
import html


def escape_html(text):
    """Escape special characters for ReportLab."""
    # Escape HTML entities
    text = html.escape(text)
    # Replace common special characters
    text = text.replace('&lt;', '<').replace('&gt;', '>')
    return text


def create_pdf_report(content, output_path, title="Policy Analysis Report"):
    """Generate formatted PDF from markdown-style text content."""
    
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                           topMargin=0.75*inch, bottomMargin=0.75*inch,
                           leftMargin=0.75*inch, rightMargin=0.75*inch)
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    styles.add(ParagraphStyle(name='CustomTitle', parent=styles['Heading1'],
                             fontSize=18, textColor=HexColor('#1a1a1a'),
                             spaceAfter=12, alignment=TA_CENTER, bold=True))
    
    styles.add(ParagraphStyle(name='CustomHeading1', parent=styles['Heading1'],
                             fontSize=14, textColor=HexColor('#2c3e50'),
                             spaceAfter=10, spaceBefore=12, bold=True))
    
    styles.add(ParagraphStyle(name='CustomHeading2', parent=styles['Heading2'],
                             fontSize=12, textColor=HexColor('#34495e'),
                             spaceAfter=8, spaceBefore=10, bold=True))
    
    styles.add(ParagraphStyle(name='CustomBody', parent=styles['BodyText'],
                             fontSize=10, alignment=TA_JUSTIFY, spaceAfter=6))
    
    styles.add(ParagraphStyle(name='CustomBullet', parent=styles['BodyText'],
                             fontSize=10, leftIndent=20, spaceAfter=4))
    
    story = []
    
    # Parse content
    lines = content.split('\n')
    
    for line in lines:
        line = line.rstrip()
        
        # Skip separator lines
        if re.match(r'^[=\-]{3,}$', line):
            story.append(Spacer(1, 0.1*inch))
            continue
        
        # Title (all caps lines or lines with many =)
        if line.isupper() and len(line) > 10 and not line.startswith((' ', '\t', '-', '*', '•')):
            story.append(Spacer(1, 0.15*inch))
            story.append(Paragraph(escape_html(line), styles['CustomTitle']))
            continue
        
        # Headings (lines ending with : or starting with **)
        if line.endswith(':') and len(line) < 80 and not line.startswith((' ', '\t')):
            story.append(Paragraph(escape_html(line), styles['CustomHeading2']))
            continue
        
        # Bold sections (**text**)
        if '**' in line:
            # Properly handle bold markdown
            clean_line = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', line)
            story.append(Paragraph(escape_html(clean_line).replace('&lt;b&gt;', '<b>').replace('&lt;/b&gt;', '</b>'), styles['CustomHeading2']))
            continue
        
        # Bullet points
        if line.strip().startswith(('-', '*', '•')):
            clean_line = line.strip().lstrip('-*• ')
            story.append(Paragraph(f"• {escape_html(clean_line)}", styles['CustomBullet']))
            continue
        
        # Numbered lists
        if re.match(r'^\s*\d+\.', line):
            story.append(Paragraph(escape_html(line.strip()), styles['CustomBullet']))
            continue
        
        # Regular paragraphs
        if line.strip():
            story.append(Paragraph(escape_html(line), styles['CustomBody']))
        else:
            story.append(Spacer(1, 0.1*inch))
    
    doc.build(story)


def generate_all_pdfs(results, output_base):
    """Generate PDF versions of all analysis reports."""
    
    pdf_files = []
    
    # Gap Analysis PDF
    gap_pdf = f"{output_base}_gap_analysis.pdf"
    create_pdf_report(results['gap_analysis'], gap_pdf, "Gap Analysis Report")
    pdf_files.append(gap_pdf)
    
    # Revised Policy PDF
    policy_pdf = f"{output_base}_revised_policy.pdf"
    create_pdf_report(results['revised_policy'], policy_pdf, "Revised Policy Document")
    pdf_files.append(policy_pdf)
    
    # Roadmap PDF
    roadmap_pdf = f"{output_base}_roadmap.pdf"
    create_pdf_report(results['roadmap'], roadmap_pdf, "Implementation Roadmap")
    pdf_files.append(roadmap_pdf)
    
    # Executive Summary PDF
    exec_pdf = f"{output_base}_executive_summary.pdf"
    create_pdf_report(results['executive_summary'], exec_pdf, "Executive Summary")
    pdf_files.append(exec_pdf)
    
    # Comprehensive Report PDF
    comprehensive = f"""
{'='*80}
COMPREHENSIVE POLICY ANALYSIS REPORT
{'='*80}
Policy: {results['policy_name']}
Analysis Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Framework: NIST Cybersecurity Framework (CIS MS-ISAC 2024)
{'='*80}

{results['executive_summary']}

{'='*80}
DETAILED GAP ANALYSIS
{'='*80}

{results['gap_analysis']}

{'='*80}
REVISED POLICY DOCUMENT
{'='*80}

{results['revised_policy']}

{'='*80}
IMPLEMENTATION ROADMAP
{'='*80}

{results['roadmap']}

{'='*80}
END OF REPORT
{'='*80}
"""
    
    comprehensive_pdf = f"{output_base}_comprehensive_report.pdf"
    create_pdf_report(comprehensive, comprehensive_pdf, "Comprehensive Policy Analysis")
    pdf_files.append(comprehensive_pdf)
    
    return pdf_files
