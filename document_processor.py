"""
document_processor.py
----------------------
Handles the data processing part of the pipeline:
- Loads a PDF file
- Extracts raw text
- Splits it into overlapping chunks
- Preserves source file and page number metadata
"""

import os

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def load_and_split_pdf(
    file_path: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
):
    """
    Loads a PDF and splits it into text chunks ready for embedding.

    Each chunk keeps:
    - source_file
    - page_number

    Page numbers are converted from zero-based PDF metadata
    to human-readable one-based page numbers.
    """

    loader = PyPDFLoader(file_path)
    raw_documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = splitter.split_documents(raw_documents)

    source_file = os.path.basename(file_path)

    for chunk in chunks:
        chunk.metadata["source_file"] = source_file

        # PyPDFLoader uses zero-based page numbers.
        page = chunk.metadata.get("page")

        if page is not None:
            chunk.metadata["page_number"] = int(page) + 1

    print(
        f"[document_processor] Loaded '{file_path}' -> "
        f"{len(chunks)} chunks"
    )

    return chunks