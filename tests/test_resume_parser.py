import unittest
import io
from unittest.mock import patch, MagicMock
from tools.resume_parser import parse_resume_file, extract_text_from_txt, extract_text_from_pdf

class TestResumeParser(unittest.TestCase):
    def test_txt_extraction_returns_string(self):
        # Text at least 150 characters
        text_content = "This is a realistic resume content that has more than one hundred and fifty characters to pass the validation check. It includes experience as a software engineer and skills in Python and Java. More filler text to reach the required length for the test case."
        file_bytes = text_content.encode('utf-8')
        
        # Mocking Streamlit UploadedFile behavior
        mock_file = MagicMock()
        mock_file.name = "resume.txt"
        mock_file.type = "text/plain"
        mock_file.read.return_value = file_bytes
        
        result = parse_resume_file(mock_file)
        self.assertIsInstance(result, str)
        self.assertIn("software engineer", result)
        self.assertIn("Python", result)

    def test_unsupported_file_type_raises_value_error(self):
        mock_file = MagicMock()
        mock_file.name = "resume.docx"
        
        with self.assertRaisesRegex(ValueError, "Unsupported file type"):
            parse_resume_file(mock_file)

    def test_empty_file_raises_value_error(self):
        mock_file = MagicMock()
        mock_file.name = "resume.txt"
        mock_file.read.return_value = b"Too short."
        
        with self.assertRaisesRegex(ValueError, "too short"):
            parse_resume_file(mock_file)

    def test_utf8_fallback_to_latin1(self):
        # Create bytes that are valid latin-1 but not valid utf-8
        latin1_content = b"Resume with special char \xa9 and enough length to pass the validation check if needed, though we call the extractor directly here."
        file_obj = MagicMock()
        file_obj.read.return_value = latin1_content
        
        result = extract_text_from_txt(file_obj)
        self.assertIsInstance(result, str)
        self.assertIn("\xa9", result)

    @patch('PyPDF2.PdfReader')
    def test_pdf_encrypted_raises_value_error(self, mock_pdf_reader):
        mock_reader_inst = MagicMock()
        mock_reader_inst.is_encrypted = True
        mock_pdf_reader.return_value = mock_reader_inst
        
        mock_file = MagicMock()
        # Ensure it has a name ending in .pdf
        mock_file.name = "test.pdf"
        
        with self.assertRaisesRegex(ValueError, "password protected"):
            extract_text_from_pdf(mock_file)

if __name__ == '__main__':
    unittest.main()
