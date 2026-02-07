"""Roadmap generator for creating NIST-aligned improvement plans."""

from gap_analyzer import call_local_llm


def generate_improvement_roadmap(gap_analysis, policy_type):
    """Generate structured improvement roadmap aligned with NIST framework."""
    
    prompt = f"""You are a cybersecurity implementation strategist. Based on the gap analysis below, create a detailed implementation roadmap for improving the {policy_type} policy aligned with the NIST Cybersecurity Framework.

GAP ANALYSIS:
{gap_analysis}

Create a comprehensive roadmap with the following structure:

POLICY IMPROVEMENT ROADMAP
==========================
Policy: {policy_type}
Framework: NIST Cybersecurity Framework

PHASE 1: IMMEDIATE ACTIONS (0-3 months)
Priority: Critical gaps requiring immediate attention
- Action 1: [Specific action]
  - NIST Function: [Identify/Protect/Detect/Respond/Recover]
  - Resources Required: [People, tools, budget]
  - Success Criteria: [Measurable outcome]
  
- Action 2: [Specific action]
  ...

PHASE 2: SHORT-TERM IMPROVEMENTS (3-6 months)
Priority: Significant gaps and process enhancements
- Action 1: [Specific action]
  ...

PHASE 3: LONG-TERM ENHANCEMENTS (6-12 months)
Priority: Minor gaps and optimization
- Action 1: [Specific action]
  ...

NIST FRAMEWORK ALIGNMENT
- Identify (ID): [Specific improvements]
- Protect (PR): [Specific improvements]
- Detect (DE): [Specific improvements]
- Respond (RS): [Specific improvements]
- Recover (RC): [Specific improvements]

KEY MILESTONES
- Month 1: [Milestone]
- Month 3: [Milestone]
- Month 6: [Milestone]
- Month 12: [Milestone]

RESOURCE REQUIREMENTS
- Personnel: [Roles needed]
- Technology: [Tools/systems needed]
- Budget: [Estimated costs]
- Training: [Training requirements]

SUCCESS METRICS
- [Metric 1]: [Target]
- [Metric 2]: [Target]
- [Metric 3]: [Target]

Be specific and actionable in all recommendations."""

    return call_local_llm(prompt)


def generate_executive_summary(gap_analysis, roadmap):
    """Generate executive summary for leadership."""
    
    prompt = f"""Create a concise executive summary for senior management based on the gap analysis and improvement roadmap below.

GAP ANALYSIS:
{gap_analysis[:1500]}...

IMPROVEMENT ROADMAP:
{roadmap[:1500]}...

Provide an executive summary in this format:

EXECUTIVE SUMMARY
=================

CURRENT STATE:
[2-3 sentences on current policy status]

KEY FINDINGS:
- [Critical finding 1]
- [Critical finding 2]
- [Critical finding 3]

RISK EXPOSURE:
[Brief description of risks from identified gaps]

RECOMMENDED ACTIONS:
[Top 3-5 priority actions]

INVESTMENT REQUIRED:
[High-level resource needs]

EXPECTED OUTCOMES:
[Benefits of implementing improvements]

TIMELINE:
[Overall implementation timeframe]

Keep it concise and business-focused for executive audience."""

    return call_local_llm(prompt)
