import fitz  # PyMuPDF
import psycopg2
from typing import List

def extract_text_from_pdf(pdf_path: str) -> List[str]:
    """Extract text from a PDF file."""
    doc = fitz.open(pdf_path)
    texts = [page.get_text() for page in doc]
    doc.close()
    return texts

def insert_pdf_text_to_db(db_conn_params: dict, pdf_texts: List[str], document_name: str):
    """Insert extracted texts from a PDF into the database."""
    conn = psycopg2.connect(**db_conn_params)
    cursor = conn.cursor()
    
    for page_number, text in enumerate(pdf_texts, start=1):
        cursor.execute(
            "INSERT INTO pdf_contents (document_name, page_number, content) VALUES (%s, %s, %s)",
            (document_name, page_number, text)
        )
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    db_conn_params = {
        "dbname": "your_database_name",
        "user": "your_database_user",
        "password": "your_database_password",
        "host": "your_database_host"
    }
    
    pdf_path = "/path/to/your/pdf/document.pdf"
    document_name = "Example Document"
    
    pdf_texts = extract_text_from_pdf(pdf_path)
    insert_pdf_text_to_db(db_conn_params, pdf_texts, document_name)

# SQL script to create the table for storing PDF contents
'''
CREATE TABLE pdf_contents (
    id SERIAL PRIMARY KEY,
    document_name VARCHAR(255),
    page_number INTEGER,
    content TEXT
);
'''