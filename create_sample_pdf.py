from fpdf import FPDF
import re

class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVu', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def write_with_superscript(pdf, text):
    """
    Writes text to the PDF, handling superscript characters.
    """
    for char in text:
        if char.isdigit() and  ord(char) > 175 : # Check for superscript digits
            pdf.char_vpos = "SUP"
            pdf.write(5, chr(ord(char) - 112)) # Convert to normal digit
            pdf.char_vpos = "LINE"
        else:
            pdf.write(5, char)


def create_sample_pdf(path):
    """
    Creates a sample PDF with footnotes for testing purposes.
    """
    pdf = PDF()
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf')
    pdf.add_font('DejaVu', 'I', 'DejaVuSans-Oblique.ttf')
    pdf.add_font('DejaVu', 'B', 'DejaVuSans-Bold.ttf')
    pdf.add_font('DejaVu', 'BI', 'DejaVuSans-BoldOblique.ttf')
    pdf.add_page()
    pdf.set_font('DejaVu', '', 12)

    # Add body text with footnote references
    write_with_superscript(pdf, 'This is the first sentence of the document, and it contains a reference to the first footnote¹.')
    pdf.ln()
    write_with_superscript(pdf, 'Here is another sentence with a second footnote reference².')
    pdf.ln()
    write_with_superscript(pdf, 'A third reference³ can be found in this line.')
    pdf.ln()

    # Add footnotes at the bottom of the page
    pdf.set_y(-50) # Position at 5 cm from the bottom
    pdf.set_font('DejaVu', '', 10)
    write_with_superscript(pdf, '¹ This is the first footnote, providing more detail.')
    pdf.ln()
    write_with_superscript(pdf, '² The second footnote is here, with additional information.')
    pdf.ln()
    write_with_superscript(pdf, '³ And finally, the third footnote appears here.')
    pdf.ln()

    pdf.output(path)

if __name__ == '__main__':
    create_sample_pdf('sample.pdf')
