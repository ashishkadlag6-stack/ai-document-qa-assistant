"""
watcher.py
-----------
Automation component: watches the 'documents' folder and automatically
processes any new PDF dropped into it, without needing a manual API call.

This covers the "automation" requirement from AI Engineer job descriptions —
it demonstrates building an automated pipeline, not just a one-off script.

Run with:
    python watcher.py
(keep it running in a separate terminal while your API is also running)
"""

import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from document_processor import load_and_split_pdf
from rag_pipeline import build_or_update_vectorstore

DOCUMENTS_FOLDER = os.getenv("DOCUMENTS_FOLDER", "documents")


class NewPDFHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if not event.src_path.lower().endswith(".pdf"):
            return

        print(f"[watcher] New file detected: {event.src_path}")
        # Small delay to make sure the file is fully written to disk before reading
        time.sleep(1)

        try:
            chunks = load_and_split_pdf(event.src_path)
            build_or_update_vectorstore(chunks)
            print(f"[watcher] Successfully auto-processed: {event.src_path}")
        except Exception as e:
            print(f"[watcher] Failed to process {event.src_path}: {e}")


if __name__ == "__main__":
    os.makedirs(DOCUMENTS_FOLDER, exist_ok=True)

    event_handler = NewPDFHandler()
    observer = Observer()
    observer.schedule(event_handler, DOCUMENTS_FOLDER, recursive=False)
    observer.start()

    print(f"[watcher] Watching '{DOCUMENTS_FOLDER}' folder for new PDFs... (Ctrl+C to stop)")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n[watcher] Stopped.")
    observer.join()
