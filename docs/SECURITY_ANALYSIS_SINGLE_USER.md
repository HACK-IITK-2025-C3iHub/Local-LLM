# Security Analysis - Single-User Local Deployment

## Context
This tool is designed for **single-user, local-only deployment**. The user runs it on their own machine to analyze their own policy documents. This significantly reduces the attack surface.

---

## ✅ NON-ISSUES (Not Applicable for Single-User Local Use)

### ❌ Rate Limiting - NOT NEEDED
**Reason:** Single user on local machine, no concurrent access

### ❌ Multi-User Access Control - NOT NEEDED
**Reason:** Only one user has access to their own machine

### ❌ Authentication/Authorization - NOT NEEDED
**Reason:** User already authenticated to their OS

### ❌ Session Management - NOT NEEDED
**Reason:** No web interface, no sessions

### ❌ CSRF/XSS - NOT NEEDED
**Reason:** CLI tool, not a web application

---

## 🔴 ACTUAL VULNERABILITIES (Single-User Context)

### 1. **Path Traversal - REAL RISK**
**Severity:** HIGH  
**File:** `src/utils.py`, `src/main.py`

**Why it matters for single user:**
- User might accidentally specify wrong path
- Typo could read sensitive system files
- Could accidentally overwrite important files

**Vulnerable Code:**
```python
# User types: python main.py --policy "../../../etc/passwd"
# System reads /etc/passwd instead of policy
```

**Real Risk:**
- Accidental data exposure
- Accidental file corruption
- User confusion from unexpected behavior

**Fix:**
```python
import os
from pathlib import Path

def validate_policy_path(file_path):
    """Validate policy file path for safety."""
    path = Path(file_path).resolve()
    
    # Check file exists
    if not path.exists():
        raise FileNotFoundError(f"Policy file not found: {file_path}")
    
    # Check it's a file, not directory
    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")
    
    # Check extension
    if path.suffix.lower() not in ['.txt', '.pdf', '.docx']:
        raise ValueError(f"Unsupported file type: {path.suffix}")
    
    # Warn if outside expected directories
    cwd = Path.cwd()
    if not str(path).startswith(str(cwd)):
        print(f"WARNING: Reading file outside project directory: {path}")
        response = input("Continue? (yes/no): ")
        if response.lower() != 'yes':
            raise ValueError("Operation cancelled by user")
    
    return str(path)
```

---

### 2. **Malicious PDF/DOCX Files - REAL RISK**
**Severity:** HIGH  
**File:** `src/utils.py:14-27`

**Why it matters for single user:**
- User might analyze policy from untrusted source
- Malicious PDF could exploit PyPDF2 vulnerabilities
- Malicious DOCX could contain macros or exploits

**Vulnerable Code:**
```python
def read_pdf_file(file_path):
    text = []
    with open(file_path, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)  # No validation
        for page in pdf_reader.pages:
            text.append(page.extract_text())
```

**Real Risk:**
- PDF with embedded malware
- DOCX with malicious macros
- Zip bomb in DOCX (DOCX is ZIP format)
- Memory exhaustion from crafted files

**Fix:**
```python
import os

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
MAX_PAGES = 500

def read_pdf_file(file_path):
    """Read PDF with safety checks."""
    # Check file size
    file_size = os.path.getsize(file_path)
    if file_size > MAX_FILE_SIZE:
        raise ValueError(f"PDF file too large: {file_size} bytes (max: {MAX_FILE_SIZE})")
    
    text = []
    try:
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            
            # Check page count
            num_pages = len(pdf_reader.pages)
            if num_pages > MAX_PAGES:
                raise ValueError(f"PDF has too many pages: {num_pages} (max: {MAX_PAGES})")
            
            # Extract text with error handling
            for i, page in enumerate(pdf_reader.pages):
                try:
                    text.append(page.extract_text())
                except Exception as e:
                    print(f"Warning: Could not extract text from page {i+1}: {e}")
                    text.append(f"[Page {i+1} - extraction failed]")
        
        return '\n'.join(text)
        
    except PyPDF2.errors.PdfReadError as e:
        raise ValueError(f"Invalid or corrupted PDF file: {e}")
    except Exception as e:
        raise ValueError(f"Error reading PDF: {e}")

def read_docx_file(file_path):
    """Read DOCX with safety checks."""
    # Check file size
    file_size = os.path.getsize(file_path)
    if file_size > MAX_FILE_SIZE:
        raise ValueError(f"DOCX file too large: {file_size} bytes")
    
    try:
        doc = Document(file_path)
        
        # Limit paragraph count
        if len(doc.paragraphs) > 10000:
            raise ValueError("DOCX has too many paragraphs")
        
        return '\n'.join([p.text for p in doc.paragraphs])
        
    except Exception as e:
        raise ValueError(f"Error reading DOCX: {e}")
```

---

### 3. **Subprocess Timeout - REAL RISK**
**Severity:** MEDIUM  
**File:** `src/gap_analyzer.py:15-22`

**Why it matters for single user:**
- LLM could hang indefinitely
- User's machine becomes unresponsive
- Wasted time waiting for stuck process

**Vulnerable Code:**
```python
def call_local_llm(prompt, model="mistral:7b-instruct"):
    result = subprocess.run(
        ['ollama', 'run', model],
        input=prompt,
        capture_output=True,
        text=True,
        encoding='utf-8'
    )  # No timeout!
```

**Real Risk:**
- Process hangs forever
- User has to kill process manually
- Lost work if analysis was running for hours

**Fix:**
```python
def call_local_llm(prompt, model="mistral:7b-instruct"):
    """Call local LLM with timeout protection."""
    TIMEOUT = 600  # 10 minutes
    
    try:
        result = subprocess.run(
            ['ollama', 'run', model],
            input=prompt,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=TIMEOUT
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"LLM failed: {result.stderr}")
        
        return result.stdout.strip()
        
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"LLM timed out after {TIMEOUT} seconds. Try a shorter policy or smaller model.")
    except FileNotFoundError:
        raise RuntimeError("Ollama not found. Please install: https://ollama.ai/download")
```

---

### 4. **Prompt Size Limits - REAL RISK**
**Severity:** MEDIUM  
**File:** `src/gap_analyzer.py:27-56`

**Why it matters for single user:**
- Very large policy could crash LLM
- Out of memory errors
- System becomes unresponsive

**Vulnerable Code:**
```python
def analyze_policy_gaps(policy_content, nist_framework):
    prompt = f"""...\n{policy_content}\n..."""  # No size check
    return call_local_llm(prompt)
```

**Real Risk:**
- 100-page policy = huge prompt
- LLM runs out of memory
- System crash or hang

**Fix:**
```python
MAX_POLICY_SIZE = 50000  # ~50KB, ~10-15 pages
MAX_PROMPT_SIZE = 100000  # Total prompt size

def analyze_policy_gaps(policy_content, nist_framework):
    """Analyze policy with size limits."""
    
    # Check policy size
    if len(policy_content) > MAX_POLICY_SIZE:
        print(f"WARNING: Policy is very large ({len(policy_content)} chars)")
        print(f"Truncating to first {MAX_POLICY_SIZE} characters")
        policy_content = policy_content[:MAX_POLICY_SIZE] + "\n\n[TRUNCATED - Policy too long]"
    
    # Build prompt
    prompt = f"""You are a cybersecurity policy analyst...
    
NIST FRAMEWORK STANDARDS:
{nist_framework}

ORGANIZATIONAL POLICY TO ANALYZE:
{policy_content}

..."""
    
    # Check total prompt size
    if len(prompt) > MAX_PROMPT_SIZE:
        raise ValueError(f"Prompt too large: {len(prompt)} chars. Please use a shorter policy.")
    
    return call_local_llm(prompt)
```

---

### 5. **Output Directory Creation - REAL RISK**
**Severity:** LOW  
**File:** `src/utils.py:44-47`

**Why it matters for single user:**
- Could accidentally create directories in wrong location
- Typo in output path could clutter filesystem

**Vulnerable Code:**
```python
def save_output(content, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Creates any path!
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
```

**Real Risk:**
- `--output "../../../tmp/malicious"` creates unexpected directories
- Clutters filesystem with typos

**Fix:**
```python
def save_output(content, output_path):
    """Save output with path validation."""
    output_dir = os.path.dirname(output_path)
    
    # Validate output directory is within project
    abs_output = Path(output_dir).resolve()
    project_root = Path.cwd()
    
    if not str(abs_output).startswith(str(project_root)):
        print(f"WARNING: Output directory outside project: {abs_output}")
        response = input("Continue? (yes/no): ")
        if response.lower() != 'yes':
            raise ValueError("Operation cancelled")
    
    # Create directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Write file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Saved: {output_path}")
```

---

### 6. **Error Message Information Leakage - LOW RISK**
**Severity:** LOW  
**File:** `src/main.py:189-191`

**Why it matters for single user:**
- Full stack traces in error messages
- Could confuse user
- Makes debugging harder

**Fix:**
```python
def main():
    try:
        # ... existing code
    except FileNotFoundError as e:
        print(f"ERROR: File not found - {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"ERROR: Invalid input - {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"ERROR: Unexpected error occurred", file=sys.stderr)
        print(f"Details: {type(e).__name__}: {e}", file=sys.stderr)
        print("Please check your input files and try again", file=sys.stderr)
        sys.exit(1)
```

---

## 📋 Priority Fixes for Single-User Deployment

### **Must Fix (High Priority)**
1. ✅ Add subprocess timeout (prevents hanging)
2. ✅ Validate file sizes (prevents memory issues)
3. ✅ Add prompt size limits (prevents crashes)
4. ✅ Validate file paths (prevents accidents)

### **Should Fix (Medium Priority)**
5. ✅ Improve error messages (better UX)
6. ✅ Add file type validation (prevents confusion)
7. ✅ Validate output paths (prevents accidents)

### **Nice to Have (Low Priority)**
8. Add progress indicators for long operations
9. Add ability to cancel long-running operations
10. Add file integrity warnings for untrusted sources

---

## 🛠️ Minimal Security Patch

Here's a minimal patch that addresses the critical issues:

```python
# Add to src/utils.py
import os
from pathlib import Path

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

def validate_file_path(file_path):
    """Basic file validation."""
    path = Path(file_path).resolve()
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not path.is_file():
        raise ValueError(f"Not a file: {file_path}")
    
    if path.suffix.lower() not in ['.txt', '.pdf', '.docx']:
        raise ValueError(f"Unsupported file type: {path.suffix}")
    
    if os.path.getsize(file_path) > MAX_FILE_SIZE:
        raise ValueError(f"File too large (max 50MB)")
    
    return str(path)

# Update read_policy_document
def read_policy_document(file_path):
    """Read policy document with validation."""
    validated_path = validate_file_path(file_path)
    ext = Path(validated_path).suffix.lower()
    
    try:
        if ext == '.txt':
            return read_text_file(validated_path)
        elif ext == '.pdf':
            return read_pdf_file(validated_path)
        elif ext == '.docx':
            return read_docx_file(validated_path)
    except Exception as e:
        raise ValueError(f"Error reading file: {e}")
```

```python
# Add to src/gap_analyzer.py
TIMEOUT = 600  # 10 minutes
MAX_PROMPT_SIZE = 100000

def call_local_llm(prompt, model="mistral:7b-instruct"):
    """Call LLM with timeout."""
    if len(prompt) > MAX_PROMPT_SIZE:
        raise ValueError(f"Prompt too large: {len(prompt)} chars")
    
    try:
        result = subprocess.run(
            ['ollama', 'run', model],
            input=prompt,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=TIMEOUT
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"LLM failed: {result.stderr}")
        
        return result.stdout.strip()
        
    except subprocess.TimeoutExpired:
        raise RuntimeError(f"LLM timed out after {TIMEOUT}s")
    except FileNotFoundError:
        raise RuntimeError("Ollama not found. Install from: https://ollama.ai/download")
```

---

## ✅ Conclusion

For **single-user local deployment**, the main risks are:

1. **Accidental mistakes** (wrong paths, large files)
2. **System hangs** (no timeouts)
3. **Resource exhaustion** (large files/prompts)
4. **Malicious files** (if analyzing untrusted policies)

**NOT risks:** Multi-user attacks, network attacks, privilege escalation, rate limiting, authentication

**Recommendation:** Implement the minimal security patch above to prevent common user errors and system hangs.
