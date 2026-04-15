import io
import zipfile

import pandas as pd
import pytest

from app.services.whatsapp_chat_parser import extract_text_from_memory, parse_chat_to_dataframe


def _make_zip_bytes(files: dict[str, str]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zip_file:
        for name, content in files.items():
            zip_file.writestr(name, content)
    return buffer.getvalue()


def test_extract_text_from_memory_decodes_txt_bytes():
    raw_text = "01/01/2024, 10:00 - Ana: Hola"

    result = extract_text_from_memory(raw_text.encode("utf-8"), "chat.txt")

    assert result == raw_text


def test_extract_text_from_memory_reads_chat_txt_inside_zip():
    raw_text = "01/01/2024, 10:00 - Ana: Hola desde zip"
    zip_bytes = _make_zip_bytes({"Mi Chat.txt": raw_text, "foto.jpg": "bin"})

    result = extract_text_from_memory(zip_bytes, "export.zip")

    assert result == raw_text


def test_extract_text_from_memory_raises_when_zip_has_no_chat_txt():
    zip_bytes = _make_zip_bytes({"notas.txt": "contenido"})

    with pytest.raises(ValueError, match="No se"):
        extract_text_from_memory(zip_bytes, "export.zip")


def test_extract_text_from_memory_raises_for_unsupported_extension():
    with pytest.raises(ValueError, match="Formato de archivo no soportado"):
        extract_text_from_memory(b"contenido", "chat.pdf")


def test_parse_chat_to_dataframe_parses_android_export():
    raw_text = (
        "01/01/2024, 10:00 - Ana: Hola\n"
        "01/01/2024, 10:05 - Luis: Buenas\n"
    )

    df = parse_chat_to_dataframe(raw_text.encode("utf-8"), "chat.txt")

    assert list(df.columns) == ["Date", "Time", "Author", "Message", "Timestamp"]
    assert len(df) == 2
    assert df.iloc[0].to_dict()["Author"] == "Ana"
    assert df.iloc[1].to_dict()["Message"] == "Buenas"
    assert pd.api.types.is_datetime64_any_dtype(df["Timestamp"])


def test_parse_chat_to_dataframe_parses_chat_from_zip():
    raw_text = "01/01/2024, 10:00 - Ana: Hola desde zip"
    zip_bytes = _make_zip_bytes({"WhatsApp Chat.txt": raw_text})

    df = parse_chat_to_dataframe(zip_bytes, "chat.zip")

    assert len(df) == 1
    assert df.iloc[0].to_dict()["Message"] == "Hola desde zip"
    assert pd.api.types.is_datetime64_any_dtype(df["Timestamp"])


def test_parse_chat_to_dataframe_merges_multiline_messages():
    raw_text = (
        "01/01/2024, 10:00 - Ana: Primera linea\n"
        "segunda linea\n"
        "01/01/2024, 10:05 - Luis: Respuesta\n"
    )

    df = parse_chat_to_dataframe(raw_text.encode("utf-8"), "chat.txt")

    assert len(df) == 2
    assert df.iloc[0].to_dict()["Message"] == "Primera linea\nsegunda linea"


def test_parse_chat_to_dataframe_parses_ios_export():
    raw_text = (
        "[01/01/2024, 10:00:03] Ana: Hola\n"
        "[01/01/2024, 10:05:10] Luis: Buenas\n"
    )

    df = parse_chat_to_dataframe(raw_text.encode("utf-8"), "chat.txt")

    assert len(df) == 2
    assert df.iloc[0].to_dict()["Time"] == "10:00:03"
    assert df.iloc[1].to_dict()["Author"] == "Luis"


def test_parse_chat_to_dataframe_ignores_unmatched_lines_before_first_message():
    raw_text = (
        "Mensajes y llamadas estan cifrados de extremo a extremo.\n"
        "01/01/2024, 10:00 - Ana: Hola\n"
    )

    df = parse_chat_to_dataframe(raw_text.encode("utf-8"), "chat.txt")

    assert len(df) == 1
    assert df.iloc[0].to_dict()["Author"] == "Ana"
    assert df.iloc[0].to_dict()["Message"] == "Hola"


def test_parse_chat_to_dataframe_returns_empty_dataframe_when_no_message_matches():
    raw_text = "Linea suelta\nOtra linea mas\n"

    df = parse_chat_to_dataframe(raw_text.encode("utf-8"), "chat.txt")

    assert df.empty
    assert list(df.columns) == []
