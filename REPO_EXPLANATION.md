# How This Repository Works

## What this project is

This repository is an **offline cybersecurity policy analysis pipeline** powered by a local LLM through Ollama. It:

1. Reads an organization policy file (`.txt`, `.pdf`, or `.docx`)
2. Loads NIST CSF reference material from `data/reference`
3. Asks a local model to identify policy gaps
4. Asks the same model to generate a revised policy
5. Asks the model to generate an implementation roadmap and executive summary
6. Writes text outputs and formatted PDF outputs to `output/`

## High-level architecture

The orchestrator is `src/main.py` and coordinates the full flow:

- **Input handling**: document loading and validation (`src/utils.py`)
- **Gap analysis**: prompt construction + Ollama invocation (`src/gap_analyzer.py`)
- **Policy revision**: revised policy generation (`src/policy_reviser.py`)
- **Roadmapping**: implementation plan + executive summary (`src/roadmap_generator.py`)
- **Reporting**: PDF conversion and formatting (`src/pdf_generator.py`)

## End-to-end flow (single policy)

`analyze_policy()` in `src/main.py` runs a deterministic six-step pipeline:

1. **Load policy** using `read_policy_document()`.
2. **Load framework** using `load_nist_framework()` from `data/reference`.
3. **Analyze gaps** with `analyze_policy_gaps()`.
4. **Revise policy** with `revise_policy()`.
5. **Generate roadmap** with `generate_improvement_roadmap()`.
6. **Generate executive summary** with `generate_executive_summary()`.

Then it saves:

- individual text files (`*_gap_analysis.txt`, `*_revised_policy.txt`, `*_roadmap.txt`, `*_executive_summary.txt`)
- one combined text report (`*_comprehensive_report.txt`)
- matching PDFs for all of the above

Filenames include a timestamp (`YYYYMMDD_HHMMSS`) so runs do not overwrite each other.

## Detailed module behavior

### 1) `src/utils.py` (I/O and safety checks)

- Enforces `MAX_FILE_SIZE = 50MB` before reading inputs.
- Supports three input readers:
  - `read_text_file()`
  - `read_pdf_file()` using `PyPDF2`
  - `read_docx_file()` using `python-docx`
- `read_policy_document()` routes by extension and raises clear errors for unsupported formats.
- `save_output()` ensures parent directories exist before writing files.

### 2) `src/gap_analyzer.py` (LLM boundary)

- Defines runtime limits:
  - `LLM_TIMEOUT = 600` seconds
  - `MAX_PROMPT_SIZE = 100000` characters
- `call_local_llm()` is the core integration: it shells out to `ollama run gemma3:4b` via `subprocess.run()` and returns stdout.
- `load_nist_framework()` accepts either a direct file or a directory; in a directory it prefers `.txt` then `.pdf`.
- `analyze_policy_gaps()` truncates overly large policy content at 50,000 chars and builds a structured gap-analysis prompt.
- `extract_gaps_structured()` parses text headings and bullets into a dictionary (`critical`, `significant`, `minor`, `summary`) for downstream structured use.

### 3) `src/policy_reviser.py` (policy rewrite)

- `revise_policy()` sends the original policy, gap analysis, and framework text to the local model with explicit instructions to:
  - cover critical/significant gaps
  - preserve policy structure
  - add actionable controls, roles, and procedures
- `generate_revision_summary()` compares snippets from original/revised versions to summarize improvements.

### 4) `src/roadmap_generator.py` (implementation planning)

- `generate_improvement_roadmap()` prompts for a phased plan:
  - 0–3 months
  - 3–6 months
  - 6–12 months
- It explicitly requests NIST function alignment (ID/PR/DE/RS/RC), milestones, resources, and success metrics.
- `generate_executive_summary()` compresses findings into leadership-oriented language.

### 5) `src/pdf_generator.py` (report formatting)

- Converts generated text into styled PDFs with ReportLab.
- Applies basic markdown-like parsing for:
  - headings
  - separator lines
  - bullets
  - numbered lists
  - inline bold markers
- `generate_all_pdfs()` emits five PDFs mirroring text outputs plus a comprehensive report.

## CLI behavior

`src/main.py` supports:

- `--policy <path>`: analyze one policy file
- `--batch <dir>`: analyze all `.txt`, `.pdf`, and `.docx` files in a directory
- `--output <dir>`: choose output directory (default: `output`)

If neither `--policy` nor `--batch` is supplied, CLI help is printed and execution exits with code 1.

## Offline model and runtime assumptions

- The system assumes Ollama is installed locally and the model `gemma3:4b` is present.
- If Ollama is missing, or model execution fails, errors are surfaced from `call_local_llm()`.
- Because inference happens through local `ollama run`, there are no cloud API calls in the application path.

## Testing and validation utilities

`test_system.py` includes:

- `--verify-offline`: checks Ollama, model presence, no external API-call patterns in `src/*.py`, and required local data files
- `--test-all`: runs full analysis against sample policies in `data/test_policies`
- `--test-policy <path>`: tests one file end-to-end

## Important practical notes

- Inference quality and runtime depend heavily on the local model and hardware.
- Large reference files + long policies can approach prompt limits.
- Current truncation behavior is simple length-based clipping, which may cut policy context mid-section.
- The output quality is prompt-driven; if you need stricter structure, tighten prompt formats in analyzer/reviser/roadmap modules.

