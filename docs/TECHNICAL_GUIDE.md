# Technical Guide

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Dependencies and Versions](#dependencies-and-versions)
3. [Code Structure and Workflow](#code-structure-and-workflow)
4. [Prompt Engineering](#prompt-engineering)
5. [Data Flow](#data-flow)
6. [Function Reference](#function-reference)
7. [Limitations](#limitations)
8. [Future Improvements](#future-improvements)

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface (CLI)                      │
│                      src/main.py                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Document Processing Layer                   │
│                      src/utils.py                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  TXT Reader  │  │  PDF Reader  │  │ DOCX Reader  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Analysis Engine Layer                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Gap Analyzer (src/gap_analyzer.py)                  │  │
│  │  - Load NIST Framework                               │  │
│  │  - Call Local LLM                                    │  │
│  │  - Extract Structured Gaps                           │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Policy Reviser (src/policy_reviser.py)             │  │
│  │  - Generate Revised Policy                           │  │
│  │  - Create Revision Summary                           │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Roadmap Generator (src/roadmap_generator.py)       │  │
│  │  - Create Implementation Roadmap                     │  │
│  │  - Generate Executive Summary                        │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    LLM Runtime Layer                         │
│                    Ollama (Local)                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Mistral-7B-Instruct / Llama-3-8B-Instruct          │  │
│  │  - Fully Offline Operation                           │  │
│  │  - No External API Calls                             │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Storage Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ NIST         │  │ Test         │  │ Output       │     │
│  │ Framework    │  │ Policies     │  │ Reports      │     │
│  │ (Reference)  │  │ (Input)      │  │ (Results)    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### Component Interaction

```
Policy Document → Document Parser → Policy Content (Text)
                                           │
                                           ▼
NIST Framework → Framework Loader → NIST Standards (Text)
                                           │
                                           ▼
                        ┌──────────────────┴──────────────────┐
                        │                                      │
                        ▼                                      ▼
            Gap Analysis Prompt                    Policy + Standards
                        │                                      │
                        └──────────────┬───────────────────────┘
                                       │
                                       ▼
                              Local LLM (Ollama)
                                       │
                                       ▼
                              Gap Analysis Report
                                       │
                        ┌──────────────┼──────────────┐
                        │              │              │
                        ▼              ▼              ▼
                Policy Revision   Roadmap      Executive Summary
                        │              │              │
                        └──────────────┴──────────────┘
                                       │
                                       ▼
                            Comprehensive Report
                                       │
                                       ▼
                              Output Files (TXT)
```

## Dependencies and Versions

### Python Version
- **Required:** Python 3.8 or higher
- **Recommended:** Python 3.10+
- **Reason:** Modern syntax, better performance, improved type hints

### Core Dependencies

#### 1. Ollama (LLM Runtime)
- **Version:** 0.1.0+
- **Purpose:** Local LLM execution framework
- **Installation:** Download from https://ollama.ai/download
- **License:** MIT License
- **Why Ollama:**
  - Easy installation and setup
  - Fully offline operation
  - Efficient model management
  - Cross-platform support
  - No external API dependencies

#### 2. PyPDF2
- **Version:** 3.0.0+
- **Purpose:** PDF document parsing
- **Installation:** `pip install PyPDF2`
- **License:** BSD License
- **Usage:** Extracts text from PDF policy documents

#### 3. python-docx
- **Version:** 1.0.0+
- **Purpose:** DOCX document parsing
- **Installation:** `pip install python-docx`
- **License:** MIT License
- **Usage:** Extracts text from Word documents

### LLM Models

#### Recommended: Mistral-7B-Instruct
- **Size:** ~4.1GB
- **Parameters:** 7 billion
- **Context Window:** 8K tokens
- **Download:** `ollama pull mistral:7b-instruct`
- **Advantages:**
  - Excellent instruction following
  - Fast inference speed
  - Good reasoning capabilities
  - Balanced accuracy/performance

#### Alternative: Llama-3-8B-Instruct
- **Size:** ~4.7GB
- **Parameters:** 8 billion
- **Context Window:** 8K tokens
- **Download:** `ollama pull llama3:8b-instruct`
- **Advantages:**
  - Strong performance
  - Good for complex analysis
  - Slightly slower than Mistral

### System Requirements

**Minimum:**
- CPU: 4 cores, 2.0 GHz
- RAM: 8GB
- Storage: 10GB free
- OS: Windows 10, Linux (Ubuntu 20.04+), macOS 11+

**Recommended:**
- CPU: 8 cores, 3.0 GHz
- RAM: 16GB
- Storage: 20GB free (SSD preferred)
- OS: Windows 11, Linux (Ubuntu 22.04+), macOS 12+

## Code Structure and Workflow

### Module Overview

#### 1. src/main.py
**Purpose:** Main entry point and orchestration

**Key Functions:**
- `analyze_policy(policy_path, output_dir)` - Main analysis orchestrator
- `main()` - CLI argument parsing and execution

**Workflow:**
1. Parse command-line arguments
2. Load policy document
3. Load NIST framework
4. Execute gap analysis
5. Generate revised policy
6. Create implementation roadmap
7. Produce executive summary
8. Save all outputs

**Error Handling:**
- File not found errors
- LLM execution failures
- Output directory creation
- Invalid file formats

#### 2. src/utils.py
**Purpose:** Document processing utilities

**Key Functions:**
- `read_text_file(file_path)` - Read plain text
- `read_pdf_file(file_path)` - Extract text from PDF
- `read_docx_file(file_path)` - Extract text from DOCX
- `read_policy_document(file_path)` - Universal document reader
- `save_output(content, output_path)` - Save reports

**Design Decisions:**
- Single interface for multiple formats
- Automatic format detection by extension
- Error handling for corrupted files
- UTF-8 encoding for international support

#### 3. src/gap_analyzer.py
**Purpose:** Gap identification against NIST standards

**Key Functions:**
- `load_nist_framework(framework_path)` - Load reference standards
- `call_local_llm(prompt, model)` - Interface with Ollama
- `analyze_policy_gaps(policy_content, nist_framework)` - Identify gaps
- `extract_gaps_structured(gap_analysis_text)` - Parse LLM output

**LLM Integration:**
- Uses subprocess to call Ollama CLI
- Fully offline operation
- No network calls
- Synchronous execution

**Gap Classification:**
- Critical: High priority, immediate attention
- Significant: Medium priority, important improvements
- Minor: Low priority, optimization opportunities

#### 4. src/policy_reviser.py
**Purpose:** Generate improved policy versions

**Key Functions:**
- `revise_policy(policy_content, gap_analysis, nist_framework)` - Create revised policy
- `generate_revision_summary(original_policy, revised_policy)` - Summarize changes

**Approach:**
- Maintains original structure
- Adds missing sections
- Enhances weak provisions
- Incorporates NIST requirements

#### 5. src/roadmap_generator.py
**Purpose:** Create implementation plans

**Key Functions:**
- `generate_improvement_roadmap(gap_analysis, policy_type)` - Create phased plan
- `generate_executive_summary(gap_analysis, roadmap)` - Leadership summary

**Roadmap Structure:**
- Phase 1 (0-3 months): Critical gaps
- Phase 2 (3-6 months): Significant improvements
- Phase 3 (6-12 months): Long-term enhancements
- NIST alignment mapping
- Resource requirements
- Success metrics

## Prompt Engineering

### Design Principles

1. **Clear Instructions:** Explicit task definition
2. **Structured Output:** Defined format for parsing
3. **Context Injection:** NIST framework + policy content
4. **Role Assignment:** "You are a cybersecurity policy analyst"
5. **Specific Requirements:** Detailed output specifications

### Gap Analysis Prompt Template

```
You are a cybersecurity policy analyst. Compare the organizational 
policy below against the NIST Cybersecurity Framework standards and 
identify ALL gaps, weaknesses, and missing elements.

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

Be specific and reference exact NIST controls that are missing or 
inadequately addressed.
```

**Why This Works:**
- Clear role definition sets context
- Structured format enables parsing
- Priority classification aids decision-making
- NIST references ensure traceability
- Comprehensive coverage through explicit instructions

### Policy Revision Prompt Template

```
You are a cybersecurity policy expert. Revise the organizational 
policy below to address ALL identified gaps and align with NIST 
Cybersecurity Framework standards.

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

Provide the complete revised policy document with all improvements 
integrated.
```

**Design Rationale:**
- Builds on gap analysis results
- Maintains policy continuity
- Ensures actionable improvements
- Preserves organizational context

### Roadmap Generation Prompt Template

```
You are a cybersecurity implementation strategist. Based on the gap 
analysis below, create a detailed implementation roadmap for improving 
the {policy_type} policy aligned with the NIST Cybersecurity Framework.

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

[Additional phases and details...]
```

**Key Elements:**
- Phased approach for manageable implementation
- NIST function mapping for framework alignment
- Resource planning for realistic execution
- Success metrics for progress tracking

## Data Flow

### Single Policy Analysis Flow

```
1. User Input
   └─> python src/main.py --policy isms_policy.txt

2. Document Loading
   └─> read_policy_document() → Policy Text (string)

3. Framework Loading
   └─> load_nist_framework() → NIST Standards (string)

4. Gap Analysis
   ├─> Construct prompt (policy + NIST)
   ├─> call_local_llm() → Ollama subprocess
   ├─> LLM inference (1-2 minutes)
   └─> Gap Analysis Report (string)

5. Policy Revision
   ├─> Construct prompt (policy + gaps + NIST)
   ├─> call_local_llm() → Ollama subprocess
   ├─> LLM inference (2-3 minutes)
   └─> Revised Policy (string)

6. Roadmap Generation
   ├─> Construct prompt (gaps + policy type)
   ├─> call_local_llm() → Ollama subprocess
   ├─> LLM inference (1-2 minutes)
   └─> Implementation Roadmap (string)

7. Executive Summary
   ├─> Construct prompt (gaps + roadmap)
   ├─> call_local_llm() → Ollama subprocess
   ├─> LLM inference (30-60 seconds)
   └─> Executive Summary (string)

8. Output Generation
   ├─> Save gap_analysis.txt
   ├─> Save revised_policy.txt
   ├─> Save roadmap.txt
   ├─> Save executive_summary.txt
   └─> Save comprehensive_report.txt

9. Completion
   └─> Display summary and file locations
```

### Batch Processing Flow

```
1. User Input
   └─> python src/main.py --batch data/test_policies/

2. Directory Scanning
   └─> Find all .txt, .pdf, .docx files

3. For Each Policy:
   ├─> Execute Single Policy Analysis Flow
   ├─> Generate separate output files
   └─> Display progress

4. Completion
   └─> Display batch summary
```

## Function Reference

### src/main.py

#### analyze_policy(policy_path, output_dir='output')
**Purpose:** Main analysis orchestrator

**Parameters:**
- `policy_path` (str): Path to policy document
- `output_dir` (str): Output directory for reports

**Returns:**
- dict: Analysis results with all generated content

**Raises:**
- FileNotFoundError: Policy file not found
- RuntimeError: LLM execution failed
- ValueError: Unsupported file format

**Example:**
```python
result = analyze_policy('isms_policy.txt', 'output/')
print(result['policy_name'])
print(result['gap_analysis'])
```

### src/utils.py

#### read_policy_document(file_path)
**Purpose:** Universal document reader

**Parameters:**
- `file_path` (str): Path to document (.txt, .pdf, .docx)

**Returns:**
- str: Extracted text content

**Raises:**
- ValueError: Unsupported file format
- FileNotFoundError: File not found

**Example:**
```python
content = read_policy_document('policy.pdf')
```

### src/gap_analyzer.py

#### call_local_llm(prompt, model="mistral:7b-instruct")
**Purpose:** Interface with local LLM via Ollama

**Parameters:**
- `prompt` (str): Input prompt for LLM
- `model` (str): Model name (default: mistral:7b-instruct)

**Returns:**
- str: LLM response

**Raises:**
- RuntimeError: LLM execution failed

**Implementation:**
```python
result = subprocess.run(
    ['ollama', 'run', model],
    input=prompt,
    capture_output=True,
    text=True,
    encoding='utf-8'
)
return result.stdout.strip()
```

**Note:** Fully offline, no network calls

#### analyze_policy_gaps(policy_content, nist_framework)
**Purpose:** Identify policy gaps using LLM

**Parameters:**
- `policy_content` (str): Policy text
- `nist_framework` (str): NIST standards

**Returns:**
- str: Gap analysis report

**Processing Time:** 1-2 minutes

### src/policy_reviser.py

#### revise_policy(policy_content, gap_analysis, nist_framework)
**Purpose:** Generate improved policy

**Parameters:**
- `policy_content` (str): Original policy
- `gap_analysis` (str): Identified gaps
- `nist_framework` (str): NIST standards

**Returns:**
- str: Revised policy document

**Processing Time:** 2-3 minutes

### src/roadmap_generator.py

#### generate_improvement_roadmap(gap_analysis, policy_type)
**Purpose:** Create phased implementation plan

**Parameters:**
- `gap_analysis` (str): Identified gaps
- `policy_type` (str): Policy name/type

**Returns:**
- str: Implementation roadmap

**Processing Time:** 1-2 minutes

## Limitations

### 1. Model Accuracy
**Issue:** LLM outputs may contain inaccuracies or hallucinations

**Impact:**
- Gap analysis may miss some issues
- May identify false positives
- Recommendations require validation

**Mitigation:**
- Human review of all outputs
- Cross-reference with NIST framework
- Validate against existing controls
- Use as decision support, not replacement

**Expected Accuracy:** 80-90% with proper review

### 2. Processing Time
**Issue:** Analysis takes 5-8 minutes per policy

**Impact:**
- Not suitable for real-time analysis
- Batch processing can be time-consuming
- Resource intensive during execution

**Mitigation:**
- Run during off-hours
- Use batch processing overnight
- Consider smaller models for speed
- Optimize hardware (16GB RAM, SSD)

**Typical Times:**
- Gap Analysis: 1-2 minutes
- Policy Revision: 2-3 minutes
- Roadmap: 1-2 minutes
- Summary: 30-60 seconds

### 3. Hardware Requirements
**Issue:** Requires significant system resources

**Impact:**
- Minimum 8GB RAM (16GB recommended)
- CPU intensive during inference
- May slow down other applications

**Mitigation:**
- Close unnecessary applications
- Run on dedicated machine if possible
- Consider cloud VM for batch processing
- Use smaller models on limited hardware

### 4. Document Format Support
**Issue:** Complex PDF layouts may not parse correctly

**Impact:**
- Scanned PDFs require OCR
- Tables may not extract properly
- Formatting may be lost
- Multi-column layouts problematic

**Mitigation:**
- Convert to TXT format when possible
- Use OCR tools for scanned documents
- Manually review extracted text
- Prefer native text formats

**Supported Formats:**
- TXT: Full support
- PDF: Text-based PDFs only
- DOCX: Standard documents only

### 5. Language Support
**Issue:** Optimized for English policies only

**Impact:**
- Other languages may have reduced accuracy
- NIST framework is English-based
- Prompt engineering assumes English

**Mitigation:**
- Translate policies to English
- Customize prompts for other languages
- Adjust NIST framework references
- Validate outputs more carefully

### 6. Context Window Limitations
**Issue:** LLM has 8K token context limit

**Impact:**
- Very long policies may be truncated
- May miss gaps in truncated sections
- Reduced accuracy for 50+ page documents

**Mitigation:**
- Split long policies into sections
- Analyze each section separately
- Combine results manually
- Summarize policies before analysis

**Practical Limit:** ~20-30 pages per analysis

### 7. NIST Framework Coverage
**Issue:** Reference data is summarized, not complete

**Impact:**
- May not cover all NIST subcategories
- Organization-specific requirements missing
- Industry-specific controls not included

**Mitigation:**
- Customize nist_framework.txt
- Add organization-specific requirements
- Include industry standards (PCI DSS, HIPAA)
- Regular updates to reference data

### 8. No Real-Time Updates
**Issue:** NIST framework and models are static

**Impact:**
- New NIST updates not reflected
- Emerging threats not considered
- Best practices may evolve

**Mitigation:**
- Regularly update reference data
- Monitor NIST framework changes
- Update models periodically
- Supplement with current threat intelligence

## Future Improvements

### 1. Enhanced Gap Detection
**Opportunity:** Improve accuracy and coverage

**Potential Enhancements:**
- Fine-tune LLM on cybersecurity policies
- Implement ensemble approach (multiple models)
- Add rule-based validation layer
- Integrate with vulnerability databases

**Expected Impact:** 90-95% accuracy

### 2. Additional Framework Support
**Opportunity:** Support multiple compliance frameworks

**Frameworks to Add:**
- ISO 27001/27002
- GDPR compliance
- SOC 2 requirements
- PCI DSS standards
- HIPAA security rules
- CIS Controls

**Implementation:**
- Modular framework loader
- Framework selection in CLI
- Multi-framework gap analysis
- Cross-framework mapping

### 3. Performance Optimization
**Opportunity:** Reduce processing time

**Optimization Strategies:**
- Model quantization (4-bit, 8-bit)
- Batch prompt processing
- Caching common analyses
- Parallel processing for batch mode
- GPU acceleration support

**Expected Improvement:** 50-70% faster

### 4. Enhanced Reporting
**Opportunity:** Better visualization and formats

**Improvements:**
- HTML reports with interactive elements
- PDF generation with formatting
- Excel/CSV export for tracking
- Dashboard for multiple policies
- Trend analysis over time
- Compliance scoring

### 5. User Interface
**Opportunity:** Improve usability

**UI Options:**
- Web-based interface (Flask/FastAPI)
- Desktop GUI (Tkinter/PyQt)
- Progress bars and real-time updates
- Interactive report viewer
- Policy comparison tool

### 6. Integration Capabilities
**Opportunity:** Connect with other tools

**Integration Points:**
- GRC platforms
- Document management systems
- Ticketing systems (Jira)
- Version control (Git)
- CI/CD pipelines

### 7. Advanced Analytics
**Opportunity:** Deeper insights

**Analytics Features:**
- Policy maturity scoring
- Risk quantification
- Compliance trend analysis
- Benchmark against industry
- Predictive gap analysis

### 8. Collaborative Features
**Opportunity:** Team collaboration

**Features:**
- Multi-user review workflow
- Comment and annotation system
- Approval workflows
- Change tracking
- Audit trail

### 9. Automated Testing
**Opportunity:** Continuous validation

**Testing Enhancements:**
- Automated regression testing
- Gap detection accuracy metrics
- Performance benchmarking
- Integration tests
- End-to-end validation

### 10. Model Improvements
**Opportunity:** Better LLM performance

**Model Enhancements:**
- Support for larger models (13B, 70B)
- Domain-specific fine-tuning
- Retrieval-augmented generation (RAG)
- Multi-model ensemble
- Specialized security models

---

## Conclusion

This technical guide provides comprehensive documentation of the Local LLM Policy Gap Analysis system. The architecture ensures complete offline operation while maintaining effectiveness through careful prompt engineering and structured workflows.

**Key Takeaways:**
- Fully offline, privacy-focused design
- Modular architecture for maintainability
- Comprehensive error handling
- Extensible for future enhancements
- Well-documented limitations and mitigations

For implementation questions, refer to the code comments and function docstrings. For usage questions, see the User Guide.
