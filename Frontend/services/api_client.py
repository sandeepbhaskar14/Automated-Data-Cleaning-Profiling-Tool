"""
frontend/services/api_client.py
────────────────────────────────
The one and only place the frontend makes HTTP calls to the backend.

All other frontend code imports from here — no raw `requests` calls elsewhere.

Usage
-----
    from services.api_client import ApiClient
    client = ApiClient()

    ok, data = client.health()
    ok, data = client.upload_dataset("/path/to/data.csv")
    ok, data = client.dataset_info(dataset_id)
"""

import requests
from pathlib import Path

from config.settings import API_BASE_URL, API_TIMEOUT_SEC
from services.logger import get_logger

log = get_logger(__name__)


class ApiError(Exception):
    """Raised when the backend returns an unexpected status or is unreachable."""


class ApiClient:
    """
    Thin wrapper around the backend REST API.

    Every method returns a tuple: (success: bool, payload: dict).
    On network failure or non-2xx response the tuple is (False, {"error": ...}).
    """

    def __init__(self, base_url: str = API_BASE_URL, timeout: int = API_TIMEOUT_SEC):
        self._base  = base_url.rstrip("/")
        self._timeout = timeout
        log.debug("ApiClient configured — base=%s  timeout=%ds", self._base, self._timeout)

    # ── internal helpers ─────────────────────────────────────────────────────

    def _get(self, path: str) -> tuple[bool, dict]:
        url = f"{self._base}{path}"
        try:
            r = requests.get(url, timeout=self._timeout)
            return self._parse(r)
        except requests.RequestException as exc:
            log.error("GET %s failed: %s", url, exc)
            return False, {"error": str(exc)}

    def _post(self, path: str, json: dict | None = None,
              files: dict | None = None) -> tuple[bool, dict]:
        url = f"{self._base}{path}"
        try:
            r = requests.post(url, json=json, files=files, timeout=self._timeout)
            return self._parse(r)
        except requests.RequestException as exc:
            log.error("POST %s failed: %s", url, exc)
            return False, {"error": str(exc)}

    def _delete(self, path: str) -> tuple[bool, dict]:
        url = f"{self._base}{path}"
        try:
            r = requests.delete(url, timeout=self._timeout)
            return self._parse(r)
        except requests.RequestException as exc:
            log.error("DELETE %s failed: %s", url, exc)
            return False, {"error": str(exc)}

    @staticmethod
    def _parse(response: requests.Response) -> tuple[bool, dict]:
        success = response.ok
        try:
            payload = response.json()
        except ValueError:
            payload = {"raw": response.text}
        if not success:
            log.warning("Backend returned HTTP %d: %s", response.status_code, payload)
        return success, payload

    # ── public API ────────────────────────────────────────────────────────────

    def health(self) -> tuple[bool, dict]:
        """GET /api/health/ — liveness probe."""
        return self._get("/api/health/")

    # Dataset
    def upload_dataset(self, file_path: str | Path) -> tuple[bool, dict]:
        """POST /api/dataset/upload — stream a file to the backend."""
        path = Path(file_path)
        with path.open("rb") as fh:
            return self._post("/api/dataset/upload", files={"file": (path.name, fh)})

    def dataset_info(self, dataset_id: str) -> tuple[bool, dict]:
        return self._get(f"/api/dataset/{dataset_id}/info")

    def delete_dataset(self, dataset_id: str) -> tuple[bool, dict]:
        return self._delete(f"/api/dataset/{dataset_id}")

    # Cleaning
    def clean_missing(self, dataset_id: str, strategy: str = "mean") -> tuple[bool, dict]:
        return self._post(f"/api/clean/{dataset_id}/missing", json={"strategy": strategy})

    def clean_duplicates(self, dataset_id: str) -> tuple[bool, dict]:
        return self._post(f"/api/clean/{dataset_id}/duplicates")

    def clean_outliers(self, dataset_id: str, method: str = "iqr") -> tuple[bool, dict]:
        return self._post(f"/api/clean/{dataset_id}/outliers", json={"method": method})

    def clean_types(self, dataset_id: str) -> tuple[bool, dict]:
        return self._post(f"/api/clean/{dataset_id}/types")

    def clean_all(self, dataset_id: str) -> tuple[bool, dict]:
        return self._post(f"/api/clean/{dataset_id}/run_all")

    # Profiling
    def profile_summary(self, dataset_id: str) -> tuple[bool, dict]:
        return self._get(f"/api/profile/{dataset_id}/summary")

    def profile_columns(self, dataset_id: str) -> tuple[bool, dict]:
        return self._get(f"/api/profile/{dataset_id}/columns")

    def profile_quality(self, dataset_id: str) -> tuple[bool, dict]:
        return self._get(f"/api/profile/{dataset_id}/quality")

    # Reports
    def generate_report(self, dataset_id: str) -> tuple[bool, dict]:
        return self._post(f"/api/report/{dataset_id}/generate")

    def download_report(self, report_id: str) -> tuple[bool, dict]:
        return self._get(f"/api/report/{report_id}/download")

    def list_reports(self) -> tuple[bool, dict]:
        return self._get("/api/report/list")