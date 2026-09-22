"""HTTP client for the existing AI Document Q&A FastAPI service."""

import os
from typing import Any, Optional

import requests
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
REQUEST_TIMEOUT = (5, 120)


class APIClientError(Exception):
    """A user-facing error raised for expected API and transport failures."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


def _error_message(response: requests.Response) -> str:
    try:
        payload = response.json()
    except ValueError:
        payload = None

    if isinstance(payload, dict):
        detail = payload.get("detail") or payload.get("message") or payload.get("error")
        if detail:
            return str(detail)
    return response.text.strip() or f"The API returned HTTP {response.status_code}."


def _request(method: str, path: str, **kwargs: Any) -> dict[str, Any]:
    try:
        response = requests.request(
            method,
            f"{API_BASE_URL}{path}",
            timeout=REQUEST_TIMEOUT,
            **kwargs,
        )
    except requests.ConnectionError as exc:
        raise APIClientError(
            f"Could not connect to the FastAPI server at {API_BASE_URL}."
        ) from exc
    except requests.Timeout as exc:
        raise APIClientError("The API request timed out. The document or question may be taking longer than expected.") from exc
    except requests.RequestException as exc:
        raise APIClientError(f"The API request failed: {exc}") from exc

    if not response.ok:
        raise APIClientError(_error_message(response), response.status_code)

    try:
        payload = response.json()
    except ValueError as exc:
        raise APIClientError("The API returned an invalid JSON response.", response.status_code) from exc

    if not isinstance(payload, dict):
        raise APIClientError("The API returned an unexpected response format.", response.status_code)
    return payload


def check_health() -> dict[str, Any]:
    """Return the backend health payload, or raise when it is unavailable."""
    return _request("GET", "/health")


def upload_document(uploaded_file: Any) -> dict[str, Any]:
    """Upload a Streamlit UploadedFile as multipart/form-data."""
    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            "application/pdf",
        )
    }
    return _request("POST", "/upload", files=files)


def ask_question(question: str) -> dict[str, Any]:
    """Ask the backend a question and return its unmodified JSON object."""
    return _request("POST", "/ask", json={"question": question})