# Filename    : docx.py
# Author      : Jon Kelley <jonk@omg.lol>
# Description : Interactive online resume for jon-kelley.com

from docx import Document
from htmldocx import HtmlToDocx

def generate_docx(html):
    """
    converts a html document into a docx file
    """
    document = Document()
    new_parser = HtmlToDocx()
    new_parser.add_html_to_document(html, document)
    document.save('/tmp/resume.docx')
