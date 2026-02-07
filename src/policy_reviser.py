"""Policy revision module for generating improved policy versions."""

from gap_analyzer import call_local_llm


def revise_policy(policy_content, gap_analysis, nist_framework):
    """Generate revised policy addressing identified gaps."""
    
    prompt = f"""You are a cybersecurity policy expert. Revise the organizational policy below to address ALL identified gaps and align with NIST Cybersecurity Framework standards.

NIST FRAMEWORK STANDARDS:
{nist_framework}

ORIGINAL POLICY:
{policy_content}

IDENTIFIED GAPS:
{gap_analysis}

Generate a REVISED POLICY that:
1. Addresses all critical and significant gaps
2. Incorporates missing NIST requirements
3. Maintains the original policy structure
4. Adds specific, actionable provisions
5. Includes clear roles, responsibilities, and procedures

Provide the complete revised policy document with all improvements integrated."""

    return call_local_llm(prompt)


def generate_revision_summary(original_policy, revised_policy):
    """Generate summary of changes between original and revised policy."""
    
    prompt = f"""Compare the original and revised policies below and provide a concise summary of key changes and improvements made.

ORIGINAL POLICY:
{original_policy[:2000]}...

REVISED POLICY:
{revised_policy[:2000]}...

Provide a summary in this format:

REVISION SUMMARY
================

KEY IMPROVEMENTS:
1. [Major improvement 1]
2. [Major improvement 2]
3. [Major improvement 3]
...

NEW PROVISIONS ADDED:
- [New provision 1]
- [New provision 2]
...

ENHANCED SECTIONS:
- [Section 1]: [What was improved]
- [Section 2]: [What was improved]
..."""

    return call_local_llm(prompt)
