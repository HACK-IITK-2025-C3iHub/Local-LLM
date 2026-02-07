"""Utility functions for document processing and text extraction."""

import os
from pathlib import Path
import PyPDF2
from docx import Document

# Security limits
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB


def validate_file_size(file_path):
    """Validate file size before processing."""
    file_size = os.path.getsize(file_path)
    if file_size > MAX_FILE_SIZE:
        raise ValueError(f"File too large: {file_size / (1024*1024):.1f}MB (max: 50MB)")
    return file_size


def read_text_file(file_path):
    """Read plain text file."""
    validate_file_size(file_path)
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def read_pdf_file(file_path):
    """Extract text from PDF file."""
    validate_file_size(file_path)
    text = []
    try:
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                text.append(page.extract_text())
        return '\n'.join(text)
    except Exception as e:
        raise ValueError(f"Error reading PDF: {e}")


def read_docx_file(file_path):
    """Extract text from DOCX file."""
    validate_file_size(file_path)
    try:
        doc = Document(file_path)
        return '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    except Exception as e:
        raise ValueError(f"Error reading DOCX: {e}")


def read_policy_document(file_path):
    """Read policy document based on file extension."""
    # Validate file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Validate it's a file
    if not os.path.isfile(file_path):
        raise ValueError(f"Path is not a file: {file_path}")
    
    ext = Path(file_path).suffix.lower()
    
    if ext == '.txt':
        return read_text_file(file_path)
    elif ext == '.pdf':
        return read_pdf_file(file_path)
    elif ext == '.docx':
        return read_docx_file(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}. Supported: .txt, .pdf, .docx")


def save_output(content, output_path):
    """Save output to file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
