"""
frontend/services/api_client.py
────────────────────────────────
The one and only place the frontend makes HTTP calls to the backend.

All other frontend code imports from here — no raw `requests` calls elsewhere.
"""

import requests
from pathlib import Path

from config.settings import API_BASE_URL, API_TIMEOUT_SEC
from services.logger import get_logger

log = get_logger(__name__)


class ApiClient:
    """
    Thin wrapper around the backend REST API.
    Every method returns (success: bool, payload: dict).
    """

    def __init__(self, base_url: str = API_BASE_URL, timeout: int = API_TIMEOUT_SEC):
        self._base    = base_url.rstrip("/")
        self._timeout = timeout

    # ── HTTP primitives ───────────────────────────────────────────────────────

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
            log.warning("Backend HTTP %d: %s", response.status_code, payload)
        return success, payload

    # ── Health ────────────────────────────────────────────────────────────────

    def health(self) -> tuple[bool, dict]:
        return self._get("/api/health/")

    # ── Dataset ───────────────────────────────────────────────────────────────

    def upload_dataset(self, file_path: str | Path) -> tuple[bool, dict]:
        path = Path(file_path)
        with path.open("rb") as fh:
            return self._post("/api/dataset/upload", files={"file": (path.name, fh)})

    def dataset_info(self, dataset_id: str) -> tuple[bool, dict]:
        return self._get(f"/api/dataset/{dataset_id}/info")

    def delete_dataset(self, dataset_id: str) -> tuple[bool, dict]:
        return self._delete(f"/api/dataset/{dataset_id}")

    # ── Cleaning ──────────────────────────────────────────────────────────────

    def clean_missing(self, dataset_id: str,
                      strategy: str = "mean") -> tuple[bool, dict]:
        return self._post(f"/api/clean/{dataset_id}/missing",
                          json={"strategy": strategy})

    def clean_missing_cols(self, dataset_id: str,
                           threshold: float = 0.50) -> tuple[bool, dict]:
        return self._post(f"/api/clean/{dataset_id}/missing_cols",
                          json={"threshold": threshold})

    def clean_duplicates(self, dataset_id: str,
                         keep: str = "first",
                         subset: list[str] | None = None) -> tuple[bool, dict]:
        body: dict = {"keep": keep}
        if subset:
            body["subset"] = subset
        return self._post(f"/api/clean/{dataset_id}/duplicates", json=body)

    def clean_outliers(self, dataset_id: str,
                       method: str = "iqr",
                       threshold: float = 1.5,
                       action: str = "clip",
                       columns: list[str] | None = None) -> tuple[bool, dict]:
        body: dict = {"method": method, "threshold": threshold, "action": action}
        if columns:
            body["columns"] = columns
        return self._post(f"/api/clean/{dataset_id}/outliers", json=body)

    def clean_types(self, dataset_id: str) -> tuple[bool, dict]:
        return self._post(f"/api/clean/{dataset_id}/types")

    def clean_normalize(self, dataset_id: str,
                        columns: list[str] | None = None,
                        ops: list[str] | None = None) -> tuple[bool, dict]:
        body: dict = {}
        if columns:
            body["columns"] = columns
        if ops:
            body["ops"] = ops
        return self._post(f"/api/clean/{dataset_id}/normalize", json=body)

    def clean_pipeline(self, dataset_id: str,
                       steps: list[dict]) -> tuple[bool, dict]:
        return self._post(f"/api/clean/{dataset_id}/pipeline",
                          json={"steps": steps})

    def clean_all(self, dataset_id: str,
                  **kwargs) -> tuple[bool, dict]:
        return self._post(f"/api/clean/{dataset_id}/run_all", json=kwargs)

    # ── Profiling ─────────────────────────────────────────────────────────────

    def profile_summary(self, dataset_id: str) -> tuple[bool, dict]:
        return self._get(f"/api/profile/{dataset_id}/summary")

    def profile_columns(self, dataset_id: str) -> tuple[bool, dict]:
        return self._get(f"/api/profile/{dataset_id}/columns")

    def profile_quality(self, dataset_id: str) -> tuple[bool, dict]:
        return self._get(f"/api/profile/{dataset_id}/quality")

    # ── Reports ───────────────────────────────────────────────────────────────

    def generate_report(self, dataset_id: str) -> tuple[bool, dict]:
        return self._post(f"/api/report/{dataset_id}/generate")

    def download_report(self, report_id: str) -> tuple[bool, dict]:
        return self._get(f"/api/report/{report_id}/download")

    def list_reports(self) -> tuple[bool, dict]:
        return self._get("/api/report/list")