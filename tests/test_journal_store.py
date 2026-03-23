import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from journal_store import build_snapshot, init_db, save_entry


class JournalStoreTests(unittest.TestCase):
    def test_save_and_summarize_entries(self):
        with TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "moon_table.db"
            init_db(db_path)
            saved = save_entry(
                {
                    "requested_date": "2026-03-13",
                    "party_mode": "pair",
                    "appetite": "curious",
                    "bottle_profile": "custom",
                    "bottle_name": "Friday fizz",
                    "custom_bottle": {
                        "name": "Friday fizz",
                        "color": "rose",
                        "sparkle": "sparkling",
                        "body": "light",
                        "acid": 5,
                        "aroma": 4,
                        "savor": 2,
                        "fruit": 4,
                    },
                    "decision_verdict": "Open Tonight",
                    "today_signal": "Neon Bouquet",
                    "tomorrow_signal": "Soft Static",
                    "first_sip": "Bright and floral.",
                    "second_sip": "Pizza made it saltier.",
                    "verdict_note": "Would open this again.",
                },
                db_path=db_path,
            )
            snapshot = build_snapshot(limit=8, db_path=db_path)

            self.assertEqual(saved["bottle_name"], "Friday fizz")
            self.assertEqual(snapshot["summary"]["total_entries"], 1)
            self.assertEqual(len(snapshot["entries"]), 1)
            self.assertEqual(snapshot["entries"][0]["custom_bottle"]["sparkle"], "sparkling")


if __name__ == "__main__":
    unittest.main()
