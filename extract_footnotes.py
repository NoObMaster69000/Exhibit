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
    all_pointers = {}
    all_definitions = []

    for i, page in enumerate(doc):
        # Extract definitions from the bottom half of the page first
        rect = page.rect
        clip = fitz.Rect(0, rect.height / 2, rect.width, rect.height)
        text = page.get_text(clip=clip)
        page_definitions = re.findall(r'(\d+)\s(.*(?:\n(?!\d+\s).*)*)', text)
        for num, info in page_definitions:
            all_definitions.append({'exhibit_number': num, 'exhibit_info': info.strip(), 'page_number': i + 1})

        # Now, extract pointers from the full page
        blocks = page.get_text("dict")["blocks"]
        current_sentence = ""
        # Determine the baseline size for normal text
        baseline_size = 0
        try:
            for b in blocks:
                if 'lines' in b:
                    for l in b["lines"]:
                        if l["spans"]:
                            # Find the most common font size as the baseline
                            sizes = [s['size'] for s in l['spans']]
                            if sizes:
                                baseline_size = max(set(sizes), key=sizes.count)
                                break
                    if baseline_size:
                        break
        except IndexError:
            pass # No spans in this block

        if not baseline_size: # Skip pages with no text
            continue

        for b in blocks:
            if 'lines' in b:
                for l in b["lines"]:
                    for s in l["spans"]:
                        # Heuristic for footnote marker: smaller font size and numeric
                        if s["size"] < baseline_size - 1 and s['text'].strip().isdigit():
                            footnote_num = s['text'].strip()
                            if footnote_num not in all_pointers:
                                all_pointers[footnote_num] = []
                            # Look back for the sentence. This is a simplification.
                            # A more robust solution would use NLP sentence tokenization.
                            pointer_text = current_sentence.strip()
                            # Get the last sentence
                            sentences = re.split(r'(?<=[.!?])\s+', pointer_text)
                            last_sentence = sentences[-1] if sentences else ""
                            all_pointers[footnote_num].append(last_sentence)
                            current_sentence = "" # Reset
                        else:
                            current_sentence += s["text"]

    # Now, map pointers to definitions
    final_data = []
    for definition in all_definitions:
        exhibit_num = definition['exhibit_number']
        pointers = all_pointers.get(exhibit_num, [""]) # Get list of pointers for this number
        # For simplicity, we take the first pointer found for a given number.
        # A more complex document might require handling multiple references.
        pointer = pointers.pop(0) if pointers else ""

        final_data.append({
            'id': len(final_data) + 1,
            'source_file': os.path.basename(pdf_path),
            'pointer': pointer,
            'exhibit_number': exhibit_num,
            'exhibit_info': definition['exhibit_info'],
            'page_number': definition['page_number'],
            'exhibit_count': len(all_definitions)
        })


    df = pd.DataFrame(final_data)
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
