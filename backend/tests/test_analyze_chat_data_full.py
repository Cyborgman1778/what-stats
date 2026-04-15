from datetime import date
from types import SimpleNamespace

from app.services import data_analyzer


def test_analyze_chat_data_returns_full_expected_payload(comprehensive_chat_df, monkeypatch):
    fake_stopwords = SimpleNamespace(words=lambda language: ["de", "el", "la"])
    monkeypatch.setattr(data_analyzer, "stopwords", fake_stopwords)

    result = data_analyzer.analyze_chat_data(comprehensive_chat_df)

    assert result == {
        "status": "success",
        "message": "El chat se ha analizado correctamente.",
        "total_messages": 10,
        "participants": ["Ana", "Luis", "Marta"],
        "total_users": 3,
        "n_messages_per_user": {
            "Luis": 4,
            "Ana": 3,
            "Marta": 3,
        },
        "hot_hours": {
            "09:00": 2,
            "10:00": 3,
            "11:00": 2,
            "20:00": 2,
            "21:00": 1,
        },
        "messages_per_day": {
            "01/01/2024": 2,
            "02/01/2024": 3,
            "03/01/2024": 2,
            "01/02/2024": 2,
            "02/02/2024": 1,
        },
        "messages_per_month": {
            "01/2024": 7,
            "02/2024": 3,
        },
        "messages_per_year": {
            "2024": 10,
        },
        "top_messages_per_day": {
            "02/01/2024": 3,
            "01/01/2024": 2,
            "03/01/2024": 2,
            "01/02/2024": 2,
            "02/02/2024": 1,
        },
        "top_words": {
            "pizza": 10,
            "cafe": 3,
            "cine": 3,
            "viaje": 2,
            "concierto": 2,
            "plan": 1,
            "trabajo": 1,
            "playa": 1,
            "libro": 1,
            "final": 1,
        },
        "top_emojis": {
            "😀": 6,
            "😂": 3,
            "😎": 2,
        },
        "longest_messages": [
            {
                "Author": "Marta",
                "Message": "concierto pizza final 😀😂!!!!!!",
                "Length": 30,
            },
            {
                "Author": "Luis",
                "Message": "viaje concierto 😎!!!!!!!!!",
                "Length": 26,
            },
            {
                "Author": "Ana",
                "Message": "viaje pizza pizza 😎!!!!!!",
                "Length": 25,
            },
            {
                "Author": "Marta",
                "Message": "cafe libro pizza 😀!!!!",
                "Length": 22,
            },
            {
                "Author": "Ana",
                "Message": "playa pizza pizza 😂!!",
                "Length": 21,
            },
            {
                "Author": "Luis",
                "Message": "pizza trabajo 😀😀!!!!",
                "Length": 20,
            },
            {
                "Author": "Ana",
                "Message": "pizza cafe plan 😀",
                "Length": 17,
            },
            {
                "Author": "Marta",
                "Message": "cine cafe 😀!!!!",
                "Length": 15,
            },
            {
                "Author": "Luis",
                "Message": "cine pizza 😂!",
                "Length": 13,
            },
            {
                "Author": "Luis",
                "Message": "cine pizza",
                "Length": 10,
            },
        ],
        "top_streaks": [
            {
                "start": date(2024, 1, 1),
                "end": date(2024, 1, 3),
                "duration": 3,
            }
        ],
    }
