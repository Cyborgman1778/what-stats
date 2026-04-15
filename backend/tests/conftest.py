from pathlib import Path
import sys

import nltk
import pandas as pd
import pytest


BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


nltk.download = lambda *args, **kwargs: True


def _build_chat_df(entries) -> pd.DataFrame:
    rows = []
    for timestamp_str, author, message in entries:
        timestamp = pd.Timestamp(timestamp_str)
        rows.append(
            {
                "Date": timestamp.strftime("%d/%m/%Y"),
                "Time": timestamp.strftime("%H:%M"),
                "Author": author,
                "Message": message,
                "Timestamp": timestamp,
            }
        )
    return pd.DataFrame(rows)


@pytest.fixture
def sample_chat_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Date": "01/01/2024",
                "Time": "10:15",
                "Author": "Ana",
                "Message": "pizza pizza cafe \U0001F600",
                "Timestamp": pd.Timestamp("2024-01-01 10:15:00"),
            },
            {
                "Date": "01/01/2024",
                "Time": "10:45",
                "Author": "Luis",
                "Message": "pizza partido \U0001F600\U0001F600",
                "Timestamp": pd.Timestamp("2024-01-01 10:45:00"),
            },
            {
                "Date": "01/01/2024",
                "Time": "11:30",
                "Author": "Ana",
                "Message": "playa cafe concierto",
                "Timestamp": pd.Timestamp("2024-01-01 11:30:00"),
            },
            {
                "Date": "02/01/2024",
                "Time": "23:05",
                "Author": "Marta",
                "Message": "concierto pizza pizza pizza",
                "Timestamp": pd.Timestamp("2024-01-02 23:05:00"),
            },
        ]
    )


@pytest.fixture
def comprehensive_chat_df() -> pd.DataFrame:
    return _build_chat_df(
        [
            ("2024-01-01 09:00", "Ana", "pizza cafe plan 😀"),
            ("2024-01-01 09:30", "Luis", "pizza trabajo 😀😀!!!!"),
            ("2024-01-02 10:00", "Ana", "playa pizza pizza 😂!!"),
            ("2024-01-02 10:30", "Marta", "cafe libro pizza 😀!!!!"),
            ("2024-01-02 10:45", "Luis", "cine pizza"),
            ("2024-01-03 11:00", "Luis", "cine pizza 😂!"),
            ("2024-01-03 11:30", "Marta", "cine cafe 😀!!!!"),
            ("2024-02-01 20:00", "Ana", "viaje pizza pizza 😎!!!!!!"),
            ("2024-02-01 20:15", "Luis", "viaje concierto 😎!!!!!!!!!"),
            ("2024-02-02 21:00", "Marta", "concierto pizza final 😀😂!!!!!!"),
        ]
    )
