# Project Submission: Local LLM Policy Gap Analyzer

---

## 1. Solution Name

**Offline NIST Policy Gap Analyzer with Local LLM**

---

## 2. Brief Description

Our solution is a fully offline, privacy-first cybersecurity policy analysis tool that leverages a local Large Language Model (Gemma3 via Ollama) to compare organizational policies against NIST Cybersecurity Framework standards. It automatically identifies gaps, generates revised policies addressing those weaknesses, and creates phased implementation roadmaps—all without sending any data to external servers. The system supports multiple document formats (TXT, PDF, DOCX) and produces professional PDF reports suitable for executive review.

---

## 3. Unique Selling Proposition (USP)

Unlike cloud-based policy analysis tools that require sending sensitive organizational documents to third-party servers, our solution operates **100% offline** after initial setup. This ensures complete data privacy and compliance with strict data handling policies. The lightweight LLM (Gemma3) runs on standard hardware (8GB RAM), making enterprise-grade policy analysis accessible to organizations of all sizes without expensive infrastructure or subscription costs. The system provides actionable, NIST-aligned recommendations rather than generic compliance checklists.

---

## 4. Innovative Features

- **Complete Offline Operation** - Zero network calls during analysis; all processing happens locally
- **Multi-Format Support** - Accepts TXT, PDF, and DOCX policy documents as input
- **Automated Gap Analysis** - AI-powered comparison against NIST CSF 2024 standards
- **Policy Revision Generation** - Automatically produces improved policy versions addressing identified gaps
- **Phased Implementation Roadmaps** - Creates 0-3, 3-6, and 6-12 month improvement plans
- **Executive Summaries** - Leadership-ready reports with key findings and recommendations
- **Professional PDF Output** - Formatted reports with proper styling via ReportLab
- **Batch Processing** - Analyze multiple policies in a single run
- **Lightweight Requirements** - Runs on standard laptops with 8GB RAM

---

## 5. Steps Taken to Complete the Solution

### Research & Planning Phase
- Studied the NIST Cybersecurity Framework (CSF) and CIS MS-ISAC Policy Template Guide 2024 to understand compliance requirements
- Evaluated various local LLM options (Llama, Mistral, Gemma) and selected Gemma3 for optimal balance of performance and resource usage
- Designed modular architecture separating concerns: document processing, gap analysis, policy revision, roadmap generation, and output formatting

### Core Development Phase
- **Document Processing Module (`utils.py`)**: Implemented multi-format document reading with PyPDF2 for PDFs, python-docx for Word documents, and native UTF-8 for text files. Added file size validation (50MB limit) for security
- **Gap Analyzer Module (`gap_analyzer.py`)**: Built LLM integration via Ollama subprocess calls with configurable timeouts (600s) and prompt size limits (100KB). Designed structured prompts that extract critical, significant, and minor gaps with NIST control references
- **Policy Reviser Module (`policy_reviser.py`)**: Created prompts that generate complete revised policies maintaining original structure while adding missing provisions
- **Roadmap Generator Module (`roadmap_generator.py`)**: Developed phased implementation planning with NIST function alignment (Identify, Protect, Detect, Respond, Recover), resource requirements, and success metrics
- **PDF Generator Module (`pdf_generator.py`)**: Built ReportLab-based PDF generation with markdown parsing, custom styles, headers, and proper formatting

### Integration & Orchestration
- Developed main orchestrator (`main.py`) with CLI interface supporting single policy analysis, batch processing, and custom output directories
- Implemented sequential pipeline: Load → Analyze → Revise → Roadmap → Summary → Generate Reports
- Added progress indicators and timing information for user feedback

### Testing & Validation
- Created comprehensive test suite (`test_system.py`) with offline verification capabilities
- Tested with sample ISMS, Data Privacy, and Patch Management policies
- Validated output quality and NIST alignment through manual review

### Documentation
- Wrote detailed README with architecture diagrams, installation instructions, and usage examples
- Created technical documentation covering system internals and customization options

---

## 6. Challenges Faced During Development

### LLM Response Quality & Consistency
The biggest challenge was ensuring consistent, high-quality responses from the local LLM. Unlike cloud APIs with fine-tuned models, local LLMs can produce varying output quality. We addressed this by:
- Designing highly structured prompts with explicit output format requirements
- Implementing prompt size limits to prevent context overflow
- Adding timeout handling for edge cases where the model might hang

### Large Document Handling
Processing lengthy policy documents (50+ pages) within LLM context limits required implementing intelligent truncation strategies that preserve critical policy sections while staying within the 50KB policy content limit.

### PDF Formatting Complexity
Converting markdown-style LLM output to properly formatted PDFs with headers, bullet points, and consistent styling required extensive ReportLab customization and HTML escape handling to prevent rendering errors.

### Offline-First Architecture
Ensuring true offline operation meant avoiding any dependencies that phone home or require network access during runtime. We carefully audited all dependencies and implemented subprocess-based LLM calls that work without network connectivity.

---

## 7. Significant Impact

This solution democratizes enterprise-grade cybersecurity policy analysis by making it:

- **Accessible**: Organizations without dedicated security teams can now analyze their policies against industry standards
- **Affordable**: No subscription fees or cloud costs; runs on existing hardware
- **Private**: Sensitive policy documents never leave the organization's infrastructure, addressing data sovereignty concerns
- **Actionable**: Instead of generic compliance reports, organizations receive specific revised policies and implementation roadmaps
- **Scalable**: Batch processing enables organization-wide policy audits

For sectors like healthcare, finance, and government where data privacy is paramount, this tool enables NIST compliance assessment without the risk of exposing sensitive operational details to third parties.

---

## 8. Repository Link

**GitHub Repository**: `[Your GitHub URL Here]`

The repository contains:
- Complete source code in `src/` directory
- Sample policies in `data/test_policies/`
- NIST reference framework in `data/reference/`
- Comprehensive README with installation and usage instructions
- Technical documentation in `docs/` folder
- Test suite for validation

---

<p align="center">
  <strong>Made With 💗 by T-reXploit</strong>
</p>
