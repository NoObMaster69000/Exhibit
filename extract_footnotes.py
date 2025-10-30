import fitz  # PyMuPDF
import pandas as pd
import re
import os
import sys

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
    definitions = []

    for i, page in enumerate(doc):
        # Get the text from the bottom half of the page
        rect = page.rect
        clip = fitz.Rect(0, rect.height / 2, rect.width, rect.height)
        text = page.get_text(clip=clip)

        # Use regex to find all footnotes
        page_definitions = re.findall(r'(\d+)\s(.*(?:\n(?!\d+\s).*)*)', text)

        # Add the page number to each definition
        definitions.extend([(d[0], d[1], i + 1) for d in page_definitions])


    df = pd.DataFrame(definitions, columns=['exhibit_number', 'exhibit_info', 'page_number'])
    df['id'] = range(1, len(df) + 1)
    df['source_file'] = os.path.basename(pdf_path)
    df['exhibit_count'] = len(df)
    # Add a placeholder for the pointer column
    df['pointer'] = ""


    return df

if __name__ == "__main__":
    pdf_path = "sample.pdf"
    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]

    df = extract_footnotes(pdf_path)
    if not df.empty:
        print(df)
        df.to_excel("final_complete_exhibits.xlsx", index=False)
        print("Successfully exported to final_complete_exhibits.xlsx")
