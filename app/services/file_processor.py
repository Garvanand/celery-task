import PyPDF2
from docx import Document
from typing import List, BinaryIO
import magic
from ..core.config import settings

class FileProcessor:
    def __init__(self):
        self.mime = magic.Magic(mime=True)

    def validate_file_type(self, file_content: bytes) -> str:
        """Validate file type using python-magic"""
        mime_type = self.mime.from_buffer(file_content)
        if mime_type not in settings.ALLOWED_FILE_TYPES:
            raise ValueError(f"Unsupported file type: {mime_type}")
        return mime_type

    def extract_text_from_pdf(self, file: BinaryIO) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        except Exception as e:
            raise ValueError(f"Error processing PDF: {str(e)}")
        return text

    def extract_text_from_docx(self, file: BinaryIO) -> str:
        """Extract text from DOCX file"""
        text = ""
        try:
            doc = Document(file)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            raise ValueError(f"Error processing DOCX: {str(e)}")
        return text

    def process_file(self, file: BinaryIO, mime_type: str) -> str:
        """Process file based on mime type"""
        if mime_type == "application/pdf":
            return self.extract_text_from_pdf(file)
        elif mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return self.extract_text_from_docx(file)
        elif mime_type == "text/plain":
            return file.read().decode('utf-8')
        else:
            raise ValueError(f"Unsupported mime type: {mime_type}")

    def chunk_text(self, text: str, chunk_size: int = None) -> List[str]:
        """Split text into chunks of specified size"""
        if chunk_size is None:
            chunk_size = settings.CHUNK_SIZE
        
        sentences = text.replace('\n', ' ').split('.')
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            sentence = sentence.strip() + "."
            if len(current_chunk) + len(sentence) <= chunk_size:
                current_chunk += " " + sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks 