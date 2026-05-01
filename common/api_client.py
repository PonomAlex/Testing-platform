from typing import Any, Dict, Optional

import allure
import requests

from common.allure_attach import attach_json, attach_text


class APIClient:
    def __init__(self, base_url: Optional[str] = None, timeout: int = 10):
        self.base_url = (base_url or "https://jsonplaceholder.typicode.com").rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def _build_url(self, endpoint: str) -> str:
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def _attach_response(self, response: requests.Response) -> None:
        attach_text("Status code", str(response.status_code))
        attach_text("Response headers", str(dict(response.headers)))
        body_preview = response.text[:1000]
        attach_text("Response body preview", body_preview)

    @allure.step("GET {endpoint}")
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        url = self._build_url(endpoint)
        attach_json("GET params", params or {})
        response = self.session.get(url, params=params, timeout=self.timeout)
        self._attach_response(response)
        return response

    @allure.step("POST {endpoint}")
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> requests.Response:
        url = self._build_url(endpoint)
        attach_json("POST payload", data or {})
        response = self.session.post(url, json=data, timeout=self.timeout)
        self._attach_response(response)
        return response

    @allure.step("PUT {endpoint}")
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> requests.Response:
        url = self._build_url(endpoint)
        attach_json("PUT payload", data or {})
        response = self.session.put(url, json=data, timeout=self.timeout)
        self._attach_response(response)
        return response

    @allure.step("DELETE {endpoint}")
    def delete(self, endpoint: str) -> requests.Response:
        url = self._build_url(endpoint)
        response = self.session.delete(url, timeout=self.timeout)
        self._attach_response(response)
        return response
