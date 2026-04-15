from datetime import date
from types import SimpleNamespace

import pandas as pd
import pytest

from app.services import data_analyzer


def _build_chat_df(entries):
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


def test_record_new_streak_returns_expected_dates_without_grace():
    result = data_analyzer._record_new_streak(date(2024, 1, 10), 4)

    assert result == {
        "start": date(2024, 1, 7),
        "end": date(2024, 1, 10),
        "duration": 4,
    }


def test_record_new_streak_uses_provided_confirmed_finish_date():
    result = data_analyzer._record_new_streak(date(2024, 1, 9), 4)

    assert result == {
        "start": date(2024, 1, 6),
        "end": date(2024, 1, 9),
        "duration": 4,
    }


def test_get_all_chat_users_returns_unique_non_null_authors():
    chat_df = pd.DataFrame({"Author": ["Ana", None, "Luis", "Ana", "Marta"]})

    result = data_analyzer._get_all_chat_users(chat_df)

    assert result == ["Ana", "Luis", "Marta"]


def test_get_filtered_df_by_user_returns_only_requested_author(sample_chat_df):
    result = data_analyzer._get_filtered_df_by_user(sample_chat_df, "Ana")

    assert len(result) == 2
    assert result["Author"].tolist() == ["Ana", "Ana"]


def test_get_basic_stats_returns_message_and_participant_counts(sample_chat_df):
    result = data_analyzer.get_basic_stats(sample_chat_df)

    assert result == {
        "total_messages": 4,
        "participants": ["Ana", "Luis", "Marta"],
        "n_participants": 3,
    }


def test_get_messages_per_user_counts_each_author(sample_chat_df):
    result = data_analyzer.get_messages_per_user(sample_chat_df)

    assert result == {
        "n_messages_per_user": {
            "Ana": 2,
            "Luis": 1,
            "Marta": 1,
        }
    }


def test_get_hot_hours_groups_messages_for_all_users(sample_chat_df):
    result = data_analyzer.get_hot_hours(sample_chat_df)

    assert result == {
        "hot_hours": {
            "10:00": 2,
            "11:00": 1,
            "23:00": 1,
        }
    }


def test_get_hot_hours_filters_by_user(sample_chat_df):
    result = data_analyzer.get_hot_hours(sample_chat_df, "Ana")

    assert result == {
        "hot_hours": {
            "10:00": 1,
            "11:00": 1,
        }
    }


def test_get_hot_hours_returns_empty_mapping_for_unknown_user(sample_chat_df):
    result = data_analyzer.get_hot_hours(sample_chat_df, "Pepe")

    assert result == {"hot_hours": {}}


def test_get_calendar_stats_builds_all_time_groupings(sample_chat_df):
    result = data_analyzer.get_calendar_stats(sample_chat_df, top_n=1)

    assert result == {
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
        },
    }


def test_get_calendar_stats_filters_by_user(sample_chat_df):
    result = data_analyzer.get_calendar_stats(sample_chat_df, user="Ana", top_n=2)

    assert result == {
        "messages_per_day": {
            "01/01/2024": 2,
        },
        "messages_per_month": {
            "01/2024": 2,
        },
        "messages_per_year": {
            "2024": 2,
        },
        "top_messages_per_day": {
            "01/01/2024": 2,
        },
    }


def test_get_word_stats_returns_filtered_top_words(sample_chat_df, monkeypatch):
    fake_stopwords = SimpleNamespace(words=lambda language: ["de", "el", "la"])
    monkeypatch.setattr(data_analyzer, "stopwords", fake_stopwords)

    result = data_analyzer.get_word_stats(sample_chat_df, top_n=3)

    assert result == {
        "pizza": 6,
        "cafe": 2,
        "concierto": 2,
    }


def test_get_word_stats_filters_by_user(sample_chat_df, monkeypatch):
    fake_stopwords = SimpleNamespace(words=lambda language: ["de", "el", "la"])
    monkeypatch.setattr(data_analyzer, "stopwords", fake_stopwords)

    result = data_analyzer.get_word_stats(sample_chat_df, user="Ana", top_n=2)

    assert result == {
        "pizza": 2,
        "cafe": 2,
    }


def test_get_emoji_stats_returns_top_emojis(sample_chat_df):
    result = data_analyzer.get_emoji_stats(sample_chat_df, top_n=1)

    assert result == {
        "\U0001F600": 3,
    }


def test_get_emoji_stats_filters_by_user(sample_chat_df):
    result = data_analyzer.get_emoji_stats(sample_chat_df, user="Ana", top_n=1)

    assert result == {
        "\U0001F600": 1,
    }


def test_get_length_stats_returns_top_n_longest_messages(sample_chat_df):
    result = data_analyzer.get_length_stats(sample_chat_df, top_n=2)

    assert result == [
        {
            "Author": "Marta",
            "Message": "concierto pizza pizza pizza",
            "Length": len("concierto pizza pizza pizza"),
        },
        {
            "Author": "Ana",
            "Message": "playa cafe concierto",
            "Length": len("playa cafe concierto"),
        },
    ]


def test_get_length_stats_filters_by_user(sample_chat_df):
    result = data_analyzer.get_length_stats(sample_chat_df, user="Ana", top_n=1)

    assert result == [
        {
            "Author": "Ana",
            "Message": "playa cafe concierto",
            "Length": len("playa cafe concierto"),
        }
    ]


def test_get_streak_stats_returns_longest_streaks_sorted_by_duration():
    chat_df = _build_chat_df(
        [
            ("2024-01-01 10:00", "Ana", "hola"),
            ("2024-01-01 11:00", "Luis", "hola"),
            ("2024-01-02 10:00", "Ana", "hola"),
            ("2024-01-02 11:00", "Luis", "hola"),
            ("2024-01-03 10:00", "Ana", "hola"),
            ("2024-01-03 11:00", "Luis", "hola"),
            ("2024-01-05 10:00", "Ana", "hola"),
            ("2024-01-05 11:00", "Luis", "hola"),
            ("2024-01-06 10:00", "Ana", "hola"),
            ("2024-01-06 11:00", "Luis", "hola"),
            ("2024-01-07 10:00", "Ana", "hola"),
            ("2024-01-07 11:00", "Luis", "hola"),
            ("2024-01-08 10:00", "Ana", "hola"),
            ("2024-01-08 11:00", "Luis", "hola"),
        ]
    )

    result = data_analyzer.get_streak_stats(chat_df, top_n=1)

    assert result == [
        {
            "start": date(2024, 1, 5),
            "end": date(2024, 1, 8),
            "duration": 4,
        }
    ]


def test_get_streak_stats_ignores_unconfirmed_trailing_grace_day():
    chat_df = _build_chat_df(
        [
            ("2024-01-01 10:00", "Ana", "hola"),
            ("2024-01-01 11:00", "Luis", "hola"),
            ("2024-01-02 10:00", "Ana", "hola"),
            ("2024-01-02 11:00", "Luis", "hola"),
            ("2024-01-03 10:00", "Ana", "hola"),
            ("2024-01-03 11:00", "Luis", "hola"),
            ("2024-01-04 10:00", "Ana", "solo"),
            ("2024-01-06 10:00", "Ana", "hola"),
            ("2024-01-06 11:00", "Luis", "hola"),
        ]
    )

    result = data_analyzer.get_streak_stats(chat_df, top_n=1)

    assert result == [
        {
            "start": date(2024, 1, 1),
            "end": date(2024, 1, 3),
            "duration": 3,
        }
    ]


def test_analyze_chat_data_returns_empty_payload_for_empty_dataframe():
    result = data_analyzer.analyze_chat_data(pd.DataFrame())

    assert result == {
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
    }


def test_analyze_chat_data_aggregates_results_for_non_empty_dataframe(sample_chat_df, monkeypatch):
    fake_stopwords = SimpleNamespace(words=lambda language: ["de", "el", "la"])
    monkeypatch.setattr(data_analyzer, "stopwords", fake_stopwords)

    result = data_analyzer.analyze_chat_data(sample_chat_df)

    assert result["total_messages"] == 4
    assert result["total_users"] == 3
    assert result["participants"] == ["Ana", "Luis", "Marta"]
    assert result["status"] == "success"
    assert result["n_messages_per_user"] == {
        "Ana": 2,
        "Luis": 1,
        "Marta": 1,
    }
    assert result["hot_hours"] == {
        "10:00": 2,
        "11:00": 1,
        "23:00": 1,
    }
