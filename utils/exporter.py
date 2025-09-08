# utils/exporter.py
from fpdf import FPDF

def export_to_pdf(text, filename="snaxi_notes.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.output(filename)
