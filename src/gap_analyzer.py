"""Gap analysis module for identifying policy weaknesses against NIST framework."""

import subprocess
import json
from pathlib import Path

# Security limits
LLM_TIMEOUT = 600  # 10 minutes
MAX_PROMPT_SIZE = 100000  # 100KB


def load_nist_framework(framework_path):
    """Load NIST framework reference data from TXT or PDF."""
    from utils import read_policy_document
    
    # If it's a directory, find TXT or PDF file
    if Path(framework_path).is_dir():
        ref_dir = Path(framework_path)
        # Look for TXT first, then PDF
        txt_files = list(ref_dir.glob('*.txt'))
        pdf_files = list(ref_dir.glob('*.pdf'))
        
        if txt_files:
            framework_path = str(txt_files[0])
        elif pdf_files:
            framework_path = str(pdf_files[0])
        else:
            raise FileNotFoundError(f"No TXT or PDF reference files found in {framework_path}")
    
    # Use existing document reader (supports TXT and PDF)
    return read_policy_document(framework_path)


def call_local_llm(prompt, model="gemma3:4b"):
    """Call local LLM via Ollama (fully offline after model download)."""
    # Check prompt size
    if len(prompt) > MAX_PROMPT_SIZE:
        raise ValueError(f"Prompt too large: {len(prompt)} characters (max: {MAX_PROMPT_SIZE})")
    
    try:
        result = subprocess.run(
            ['ollama', 'run', model],
            input=prompt,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=LLM_TIMEOUT
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"LLM execution failed: {result.stderr}")
        
        return result.stdout.strip()
        
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"LLM execution timed out after {LLM_TIMEOUT} seconds. Try a shorter policy.")
    except FileNotFoundError:
        raise RuntimeError("Ollama not found. Please install from: https://ollama.ai/download")
    except Exception as e:
        raise RuntimeError(f"LLM execution failed: {e}")


def analyze_policy_gaps(policy_content, nist_framework):
    """Identify gaps in policy against NIST framework using local LLM."""
    
    # Truncate policy if too large
    MAX_POLICY_SIZE = 50000  # ~50KB
    if len(policy_content) > MAX_POLICY_SIZE:
        print(f"WARNING: Policy is large ({len(policy_content)} chars). Truncating to {MAX_POLICY_SIZE} chars.")
        policy_content = policy_content[:MAX_POLICY_SIZE] + "\n\n[TRUNCATED - Policy exceeded size limit]"
    
    prompt = f"""You are a cybersecurity policy analyst. Compare the organizational policy below against the NIST Cybersecurity Framework standards and identify ALL gaps, weaknesses, and missing elements.

NIST FRAMEWORK STANDARDS:
{nist_framework}

ORGANIZATIONAL POLICY TO ANALYZE:
{policy_content}

Provide a detailed gap analysis in the following format:

GAP ANALYSIS REPORT
===================

1. CRITICAL GAPS (High Priority)
[List all critical missing elements with specific references to NIST requirements]

2. SIGNIFICANT GAPS (Medium Priority)
[List all significant weaknesses and incomplete provisions]

3. MINOR GAPS (Low Priority)
[List all minor improvements needed]

4. SUMMARY
[Provide overall assessment and key findings]

Be specific and reference exact NIST controls that are missing or inadequately addressed."""

    return call_local_llm(prompt)


def extract_gaps_structured(gap_analysis_text):
    """Extract structured gap information from analysis text."""
    gaps = {
        'critical': [],
        'significant': [],
        'minor': [],
        'summary': ''
    }
    
    lines = gap_analysis_text.split('\n')
    current_section = None
    
    for line in lines:
        line = line.strip()
        if 'CRITICAL GAPS' in line.upper():
            current_section = 'critical'
        elif 'SIGNIFICANT GAPS' in line.upper():
            current_section = 'significant'
        elif 'MINOR GAPS' in line.upper():
            current_section = 'minor'
        elif 'SUMMARY' in line.upper():
            current_section = 'summary'
        elif line and current_section:
            if current_section == 'summary':
                gaps['summary'] += line + ' '
            elif line.startswith(('-', '•', '*')) or line[0].isdigit():
                gaps[current_section].append(line.lstrip('-•* 0123456789.'))
    
    return gaps
