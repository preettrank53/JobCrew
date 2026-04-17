import sys
import os

def extract_text_from_pdf(file_object):
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        raise ImportError("PyPDF2 is not installed. Please install it using 'pip install PyPDF2'")
        
    try:
        reader = PdfReader(file_object)
        if reader.is_encrypted:
            raise ValueError("PDF is password protected and cannot be parsed")
            
        pages_text = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages_text.append(text)
                
        final_text = "\n".join(pages_text).strip()
        return final_text
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise ValueError(f"PDF parsing failed: {str(e)}")

def extract_text_from_txt(file_object):
    try:
        content = file_object.read()
        try:
            text = content.decode('utf-8')
        except UnicodeDecodeError:
            try:
                text = content.decode('latin-1')
            except UnicodeDecodeError:
                raise ValueError("Failed to decode TXT file using utf-8 or latin-1 encodings")
        return text.strip()
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise ValueError(f"TXT parsing failed: {str(e)}")

def parse_resume_file(uploaded_file):
    filename = getattr(uploaded_file, 'name', '')
    if not filename:
        raise ValueError("File object does not have a 'name' attribute")
        
    ext = os.path.splitext(filename)[1].lower()
    
    if ext == '.pdf':
        text = extract_text_from_pdf(uploaded_file)
    elif ext == '.txt':
        text = extract_text_from_txt(uploaded_file)
    else:
        raise ValueError("Unsupported file type. Please upload a PDF or TXT file")
        
    if len(text) < 100:
        raise ValueError("Extracted text is too short — the file may be empty or image-based")
        
    return text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python resume_parser.py <path_to_resume_file>")
        sys.exit(1)
        
    filepath = sys.argv[1]
    try:
        with open(filepath, 'rb') as f:
            extracted_text = parse_resume_file(f)
            print("--- Extracted Text Preview ---")
            print(extracted_text[:500])
            print("--- End of Preview ---")
    except Exception as e:
        print(f"Error: {e}")
