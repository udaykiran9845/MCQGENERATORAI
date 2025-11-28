import os
import pdfplumber
from docx import Document

class DocumentParser:
    """Modular document parser for PDF, DOCX, and TXT files."""
    
    def parse(self, filepath):
        """
        Parse document based on file extension.
        
        Args:
            filepath: Path to the document file
            
        Returns:
            str: Extracted text content
        """
        ext = os.path.splitext(filepath)[1].lower()
        
        if ext == '.pdf':
            return self._parse_pdf(filepath)
        elif ext == '.docx':
            return self._parse_docx(filepath)
        elif ext == '.txt':
            return self._parse_txt(filepath)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    
    def _parse_pdf(self, filepath):
        """Extract text from PDF using pdfplumber."""
        text_content = []
        try:
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
            return '\n\n'.join(text_content)
        except Exception as e:
            raise Exception(f"Error parsing PDF: {str(e)}")
    
    def _parse_docx(self, filepath):
        """Extract text from DOCX using python-docx."""
        try:
            doc = Document(filepath)
            paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
            return '\n\n'.join(paragraphs)
        except Exception as e:
            raise Exception(f"Error parsing DOCX: {str(e)}")
    
    def _parse_txt(self, filepath):
        """Extract text from TXT file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(filepath, 'r', encoding='latin-1') as f:
                return f.read()
        except Exception as e:
            raise Exception(f"Error parsing TXT: {str(e)}")

