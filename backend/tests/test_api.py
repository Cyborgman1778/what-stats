import asyncio
import json
from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4

import pytest

from app.core.config import settings
from app.main import app
from app.services import data_analyzer


RESOURCES_DIR = Path(__file__).resolve().parent / "resources"


def _patch_stopwords(monkeypatch):
    fake_stopwords = SimpleNamespace(words=lambda language: ["de", "el", "la"])
    monkeypatch.setattr(data_analyzer, "stopwords", fake_stopwords)


def _txt_upload(raw_text: str, filename: str = "chat.txt"):
    return {"file": (filename, raw_text.encode("utf-8"), "text/plain")}


class ASGIResponse:
    def __init__(self, status_code, headers, body):
        self.status_code = status_code
        self.headers = headers
        self.body = body
        self.text = body.decode("utf-8")

    def json(self):
        return json.loads(self.text)


def _build_multipart_body(files):
    boundary = f"boundary-{uuid4().hex}"
    chunks = []

    for field_name, (filename, content, content_type) in files.items():
        chunks.extend(
            [
                f"--{boundary}\r\n".encode("utf-8"),
                (
                    f'Content-Disposition: form-data; name="{field_name}"; '
                    f'filename="{filename}"\r\n'
                ).encode("utf-8"),
                f"Content-Type: {content_type}\r\n\r\n".encode("utf-8"),
                content,
                b"\r\n",
            ]
        )

    chunks.append(f"--{boundary}--\r\n".encode("utf-8"))
    return boundary, b"".join(chunks)


def _request(method, path, *, headers=None, body=b""):
    async def _call_app():
        response_status = None
        response_headers = []
        response_body = bytearray()
        request_sent = False

        normalized_headers = []
        for key, value in (headers or {}).items():
            normalized_headers.append((key.lower().encode("latin-1"), value.encode("latin-1")))

        if body and not any(key == b"content-length" for key, _ in normalized_headers):
            normalized_headers.append((b"content-length", str(len(body)).encode("latin-1")))

        scope = {
            "type": "http",
            "asgi": {"version": "3.0"},
            "http_version": "1.1",
            "method": method,
            "scheme": "http",
            "path": path,
            "raw_path": path.encode("ascii"),
            "query_string": b"",
            "root_path": "",
            "headers": normalized_headers,
            "client": ("127.0.0.1", 50000),
            "server": ("127.0.0.1", 8000),
            "state": {},
        }

        async def receive():
            nonlocal request_sent
            if not request_sent:
                request_sent = True
                return {"type": "http.request", "body": body, "more_body": False}
            return {"type": "http.disconnect"}

        async def send(message):
            nonlocal response_status, response_headers
            if message["type"] == "http.response.start":
                response_status = message["status"]
                response_headers = message.get("headers", [])
            elif message["type"] == "http.response.body":
                response_body.extend(message.get("body", b""))

        await app(scope, receive, send)

        decoded_headers = {
            key.decode("latin-1").lower(): value.decode("latin-1")
            for key, value in response_headers
        }
        return ASGIResponse(response_status, decoded_headers, bytes(response_body))

    return asyncio.run(_call_app())


def _get(path, *, headers=None):
    return _request("GET", path, headers=headers)


def _post_multipart(path, files, *, headers=None):
    boundary, body = _build_multipart_body(files)
    multipart_headers = {
        "content-type": f"multipart/form-data; boundary={boundary}",
    }
    if headers:
        multipart_headers.update(headers)
    return _request("POST", path, headers=multipart_headers, body=body)


@pytest.fixture(autouse=True)
def reset_rate_limiter_storage():
    app.state.limiter._storage.reset()
    yield
    app.state.limiter._storage.reset()


def test_root_returns_healthcheck_message():
    response = _get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "WhatStats API funcionando. Privacidad por diseño activa."
    }


def test_upload_chat_rejects_unsupported_extension():
    response = _post_multipart(
        "/upload-chat",
        files={"file": ("chat.pdf", b"contenido", "application/pdf")},
    )

    assert response.status_code == 400
    assert "Formato no valido" in response.json()["detail"].replace("á", "a")


def test_upload_chat_returns_full_stats_for_valid_txt(monkeypatch):
    _patch_stopwords(monkeypatch)
    longest_marta = "concierto pizza pizza pizza"
    longest_ana = "playa cafe concierto"
    ana_emoji = "pizza pizza cafe 😀"
    luis_emoji = "pizza partido 😀😀"
    raw_text = (
        "01/01/2024, 10:15 - Ana: pizza pizza cafe 😀\n"
        "01/01/2024, 10:45 - Luis: pizza partido 😀😀\n"
        "01/01/2024, 11:30 - Ana: playa cafe concierto\n"
        "02/01/2024, 23:05 - Marta: concierto pizza pizza pizza\n"
    )

    response = _post_multipart("/upload-chat", _txt_upload(raw_text))

    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "stats": {
            "status": "success",
            "message": "El chat se ha analizado correctamente.",
            "total_messages": 4,
            "participants": ["Ana", "Luis", "Marta"],
            "total_users": 3,
            "n_messages_per_user": {
                "Ana": 2,
                "Luis": 1,
                "Marta": 1,
            },
            "hot_hours": {
                "10:00": 2,
                "11:00": 1,
                "23:00": 1,
            },
            "messages_per_day": {
                "01/01/2024": 3,
                "02/01/2024": 1,
            },
            "messages_per_month": {
                "01/2024": 4,
            },
            "messages_per_year": {
                "2024": 4,
            },
            "top_messages_per_day": {
                "01/01/2024": 3,
                "02/01/2024": 1,
            },
            "top_words": {
                "pizza": 6,
                "cafe": 2,
                "concierto": 2,
                "partido": 1,
                "playa": 1,
            },
            "top_emojis": {
                "😀": 3,
            },
            "longest_messages": [
                {
                    "Author": "Marta",
                    "Message": longest_marta,
                    "Length": len(longest_marta),
                },
                {
                    "Author": "Ana",
                    "Message": longest_ana,
                    "Length": len(longest_ana),
                },
                {
                    "Author": "Ana",
                    "Message": ana_emoji,
                    "Length": len(ana_emoji),
                },
                {
                    "Author": "Luis",
                    "Message": luis_emoji,
                    "Length": len(luis_emoji),
                },
            ],
            "top_streaks": [],
        },
    }


def test_upload_chat_parses_chat_from_zip_resource(monkeypatch):
    _patch_stopwords(monkeypatch)
    zip_path = RESOURCES_DIR / "chat_sintetico_extenso.zip"

    response = _post_multipart(
        "/upload-chat",
        files={"file": (zip_path.name, zip_path.read_bytes(), "application/zip")},
    )

    body = response.json()

    assert response.status_code == 200
    assert body["status"] == "success"
    assert body["stats"]["status"] == "success"
    assert body["stats"]["total_messages"] > 30
    assert "Ana" in body["stats"]["participants"]
    assert "+34 612 34 56 78" in body["stats"]["participants"]
    assert body["stats"]["top_words"]
    assert body["stats"]["longest_messages"]


def test_upload_chat_returns_failed_stats_when_parser_finds_no_messages(monkeypatch):
    _patch_stopwords(monkeypatch)

    response = _post_multipart(
        "/upload-chat",
        files=_txt_upload("Linea suelta\nOtra linea mas\n"),
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "stats": {
            "status": "failed",
            "message": "El chat analizado no contiene mensajes válidos.",
            "total_messages": 0,
            "participants": [],
            "total_users": 0,
            "n_messages_per_user": {},
            "hot_hours": {},
            "messages_per_day": {},
            "messages_per_month": {},
            "messages_per_year": {},
            "top_messages_per_day": {},
            "top_words": {},
            "top_emojis": {},
            "longest_messages": [],
            "top_streaks": [],
        },
    }


def test_upload_chat_enforces_rate_limit_after_three_requests(monkeypatch):
    _patch_stopwords(monkeypatch)
    files = _txt_upload("01/01/2024, 10:00 - Ana: hola\n")

    first = _post_multipart("/upload-chat", files)
    second = _post_multipart("/upload-chat", files)
    third = _post_multipart("/upload-chat", files)
    fourth = _post_multipart("/upload-chat", files)

    assert first.status_code == 200
    assert second.status_code == 200
    assert third.status_code == 200
    assert fourth.status_code == 429


def test_upload_chat_returns_413_when_payload_exceeds_max_size(monkeypatch):
    monkeypatch.setattr(settings, "MAX_UPLOAD_SIZE", 10)

    response = _post_multipart(
        "/upload-chat",
        files={"file": ("chat.txt", b"0123456789ABCDEF", "text/plain")},
    )

    assert response.status_code == 413
    assert response.json() == {
        "detail": "Payload Too Large: El archivo supera el límite de tamaño permitido."
    }
