import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

from app.service import SearchRequest, SearchService


def perform_search(query: str, mode: str = "skills") -> dict:
    service = SearchService()
    response = service.search(SearchRequest(query=query, mode=mode))
    return {
        "mode": response.mode,
        "ranking_mode": response.ranking_mode,
        "results": response.results,
        "messages": response.messages,
    }


class handler(BaseHTTPRequestHandler):
    def _send_json(self, payload: dict, status_code: int = 200) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:
        self._send_json({}, status_code=204)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        query = params.get("query", [""])[0]
        mode = params.get("mode", ["skills"])[0]

        if mode not in {"skills", "summary"}:
            self._send_json({"error": "Invalid mode. Use 'skills' or 'summary'."}, status_code=400)
            return

        payload = perform_search(query, mode=mode)
        self._send_json(payload)
