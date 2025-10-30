from fpdf import FPDF
from fpdf.enums import XPos, YPos

class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVu', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')

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
    pdf.write_html('This is the first sentence of the document, and it contains a reference to the first footnote<sup>1</sup>.')
    pdf.ln()
    pdf.write_html('Here is another sentence with a second footnote reference<sup>2</sup>.')
    pdf.ln()
    pdf.write_html('A third reference<sup>3</sup> can be found in this line.')
    pdf.ln()

    # Add footnotes at the bottom of the page
    pdf.set_y(-50) # Position at 5 cm from the bottom
    pdf.set_font('DejaVu', '', 10)
    pdf.write_html('<sup>1</sup> This is the first footnote, providing more detail.')
    pdf.ln()
    pdf.write_html('<sup>2</sup> The second footnote is here, with additional information.')
    pdf.ln()
    pdf.write_html('<sup>3</sup> And finally, the third footnote appears here.')
    pdf.ln()

    pdf.output(path)

if __name__ == '__main__':
    create_sample_pdf('sample.pdf')
