from __future__ import annotations

import json
import sqlite3
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "moon_table.db"
LOS_ANGELES = ZoneInfo("America/Los_Angeles")


def connect(db_path: str | Path = DB_PATH) -> sqlite3.Connection:
    connection = sqlite3.connect(str(db_path))
    connection.row_factory = sqlite3.Row
    return connection


def init_db(db_path: str | Path = DB_PATH) -> None:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with connect(path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS journal_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                requested_date TEXT NOT NULL,
                party_mode TEXT NOT NULL,
                appetite TEXT NOT NULL,
                bottle_profile_key TEXT NOT NULL,
                bottle_name TEXT NOT NULL,
                custom_bottle_json TEXT NOT NULL,
                decision_verdict TEXT NOT NULL,
                today_signal TEXT NOT NULL,
                tomorrow_signal TEXT NOT NULL,
                first_sip TEXT NOT NULL,
                second_sip TEXT NOT NULL,
                verdict_note TEXT NOT NULL
            )
            """
        )
        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_journal_entries_created_at
            ON journal_entries (created_at DESC)
            """
        )


def clean_text(value: Any, limit: int = 500) -> str:
    if not isinstance(value, str):
        return ""
    return value.strip()[:limit]


def normalize_entry(payload: dict[str, Any]) -> dict[str, Any]:
    custom_bottle = payload.get("custom_bottle")
    if not isinstance(custom_bottle, dict):
        custom_bottle = {}

    return {
        "requested_date": clean_text(payload.get("requested_date"), 32) or datetime.now(LOS_ANGELES).date().isoformat(),
        "party_mode": clean_text(payload.get("party_mode"), 24) or "pair",
        "appetite": clean_text(payload.get("appetite"), 24) or "curious",
        "bottle_profile_key": clean_text(payload.get("bottle_profile"), 32) or "none",
        "bottle_name": clean_text(payload.get("bottle_name"), 120) or "Unnamed bottle",
        "custom_bottle": custom_bottle,
        "decision_verdict": clean_text(payload.get("decision_verdict"), 80) or "Open Tonight",
        "today_signal": clean_text(payload.get("today_signal"), 80) or "Unknown",
        "tomorrow_signal": clean_text(payload.get("tomorrow_signal"), 80) or "Unknown",
        "first_sip": clean_text(payload.get("first_sip"), 900),
        "second_sip": clean_text(payload.get("second_sip"), 900),
        "verdict_note": clean_text(payload.get("verdict_note"), 900),
    }


def row_to_entry(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "created_at": row["created_at"],
        "requested_date": row["requested_date"],
        "party_mode": row["party_mode"],
        "appetite": row["appetite"],
        "bottle_profile": row["bottle_profile_key"],
        "bottle_name": row["bottle_name"],
        "custom_bottle": json.loads(row["custom_bottle_json"]),
        "decision_verdict": row["decision_verdict"],
        "today_signal": row["today_signal"],
        "tomorrow_signal": row["tomorrow_signal"],
        "first_sip": row["first_sip"],
        "second_sip": row["second_sip"],
        "verdict_note": row["verdict_note"],
    }


def save_entry(payload: dict[str, Any], db_path: str | Path = DB_PATH) -> dict[str, Any]:
    init_db(db_path)
    entry = normalize_entry(payload)
    created_at = datetime.now(LOS_ANGELES).isoformat(timespec="seconds")
    with connect(db_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO journal_entries (
                created_at,
                requested_date,
                party_mode,
                appetite,
                bottle_profile_key,
                bottle_name,
                custom_bottle_json,
                decision_verdict,
                today_signal,
                tomorrow_signal,
                first_sip,
                second_sip,
                verdict_note
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                created_at,
                entry["requested_date"],
                entry["party_mode"],
                entry["appetite"],
                entry["bottle_profile_key"],
                entry["bottle_name"],
                json.dumps(entry["custom_bottle"], separators=(",", ":")),
                entry["decision_verdict"],
                entry["today_signal"],
                entry["tomorrow_signal"],
                entry["first_sip"],
                entry["second_sip"],
                entry["verdict_note"],
            ),
        )
        saved_id = cursor.lastrowid
        row = connection.execute("SELECT * FROM journal_entries WHERE id = ?", (saved_id,)).fetchone()
    return row_to_entry(row)


def list_entries(limit: int = 8, db_path: str | Path = DB_PATH) -> list[dict[str, Any]]:
    init_db(db_path)
    with connect(db_path) as connection:
        rows = connection.execute(
            """
            SELECT *
            FROM journal_entries
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [row_to_entry(row) for row in rows]


def summarize_entries(entries: list[dict[str, Any]], db_path: str | Path = DB_PATH) -> dict[str, Any]:
    init_db(db_path)
    with connect(db_path) as connection:
        total_entries = connection.execute("SELECT COUNT(*) FROM journal_entries").fetchone()[0]
        distinct_bottles = connection.execute("SELECT COUNT(DISTINCT bottle_name) FROM journal_entries").fetchone()[0]

    if total_entries == 0:
        return {
            "total_entries": 0,
            "distinct_bottles": 0,
            "top_signal": "No archive yet",
            "top_verdict": "No verdicts yet",
            "story": "Archive a tasting and the Moon Table will start keeping a cellar memory.",
            "highlights": [
                "The first archived note becomes the seed of the cellar log.",
                "Custom bottles and fixed archetypes both save into the same archive.",
            ],
        }

    verdict_counter = Counter(entry["decision_verdict"] for entry in entries)
    signal_counter = Counter(entry["today_signal"] for entry in entries)
    appetite_counter = Counter(entry["appetite"] for entry in entries)

    top_verdict = verdict_counter.most_common(1)[0][0] if verdict_counter else "Unknown"
    top_signal = signal_counter.most_common(1)[0][0] if signal_counter else "Unknown"
    top_appetite = appetite_counter.most_common(1)[0][0] if appetite_counter else "Unknown"
    story = (
        f"{total_entries} archived tastings so far. "
        f"The recent archive leans {top_verdict.lower()} on {top_signal} nights."
    )

    return {
        "total_entries": total_entries,
        "distinct_bottles": distinct_bottles,
        "top_signal": top_signal,
        "top_verdict": top_verdict,
        "story": story,
        "highlights": [
            f"Most common appetite lately: {top_appetite}.",
            f"{distinct_bottles} different bottle names have been tested.",
            f"Latest archive signal leader: {top_signal}.",
        ],
    }


def build_snapshot(limit: int = 8, db_path: str | Path = DB_PATH) -> dict[str, Any]:
    entries = list_entries(limit=limit, db_path=db_path)
    return {
        "summary": summarize_entries(entries, db_path=db_path),
        "entries": entries,
    }
