"""
document_processor.py
----------------------
Handles the "data processing" part of the pipeline:
- Loads a PDF file
- Extracts raw text
- Splits it into overlapping chunks (better for retrieval accuracy)
"""

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def load_and_split_pdf(file_path: str, chunk_size: int = 1000, chunk_overlap: int = 150):
    """
    Loads a PDF and splits it into text chunks ready for embedding.

    Args:
        file_path: path to the PDF file on disk
        chunk_size: max characters per chunk
        chunk_overlap: overlap between chunks (helps preserve context across splits)

    Returns:
        List of LangChain Document objects (each with .page_content and .metadata)
    """
    loader = PyPDFLoader(file_path)
    raw_documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = splitter.split_documents(raw_documents)

    # Tag each chunk with its source file name, useful for citing answers later
    for chunk in chunks:
        chunk.metadata["source_file"] = file_path.split("/")[-1]

    print(f"[document_processor] Loaded '{file_path}' -> {len(chunks)} chunks")
    return chunks
