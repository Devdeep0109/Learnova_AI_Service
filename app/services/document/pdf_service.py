import fitz


def extract_text_from_pdf(file_path: str):

    doc = fitz.open(file_path)
    page_count = len(doc)
    text = ""

    for page in doc:
        text += page.get_text()
    doc.close()

    return {
        "page_count": page_count,
        "text": text
    }