import PyPDF2
from io import BytesIO


def extract_text_pdf(pdf):
    """Metodo para tomar el texto del pdf de manera correcta"""
    try:
        pdf_reader =  PyPDF2.PdfReader(BytesIO(pdf.read()))
        complete_text = ""

        for page_number, page in enumerate(pdf_reader.pages,1):
            page_text = page.extract_text()
            if page_text.strip():
                complete_text +=f"\n---- PAGE {page_number} ----\n"
                complete_text += page_text + "\n" 

        complete_text = complete_text.strip()

        if not complete_text:
            return "Error: PDF seems to be empty or only have images"
        
        return complete_text
    except Exception as e:
        return f"Error trying to process the PDF: {str(e)}"