import fitz  # PyMuPDF
import pandas as pd
import re
import os

def extract_footnotes(pdf_path):
    """
    Extracts footnotes and their references from a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        pd.DataFrame: A DataFrame containing the extracted footnote data.
    """
    if not os.path.exists(pdf_path):
        print(f"Error: The file '{pdf_path}' was not found.")
        return pd.DataFrame()

    doc = fitz.open(pdf_path)
    pointers = []
    footnote_text = ""

    for i, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        current_pointer = ""
        footnote_y_threshold = page.rect.height / 2

        for b in blocks:
            for l in b["lines"]:
                for s in l["spans"]:
                    # Check for superscript
                    if s["flags"] & 1:
                        pointers.append(re.sub(r'\s+', ' ', current_pointer.strip()))
                        current_pointer = ""
                    else:
                        current_pointer += s["text"]

                    if s["origin"][1] > footnote_y_threshold and "Page" not in s["text"]:
                        footnote_text += s["text"]

    # Split the footnote text by the footnote markers
    definitions = re.split(r'(I|B|C)', footnote_text)
    # Remove empty strings and combine the marker with the definition
    definitions = [definitions[i] + definitions[i+1] for i in range(1, len(definitions)-1, 2)]


    df = pd.DataFrame({
        'id': range(1, len(pointers) + 1),
        'source_file': os.path.basename(pdf_path),
        'pointer': pointers,
        'exhibit_info': definitions,
        'exhibit_count': len(pointers)
    })

    return df

if __name__ == "__main__":
    df = extract_footnotes("sample.pdf")
    if not df.empty:
        df.to_excel("final_complete_exhibits.xlsx", index=False)
        print("Successfully exported to final_complete_exhibits.xlsx")
