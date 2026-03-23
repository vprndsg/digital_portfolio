import unittest
from datetime import date

from engine import (
    build_experience,
    build_lunar_state,
    normalize_appetite,
    normalize_bottle_profile,
    normalize_custom_bottle,
    normalize_party_mode,
)


class EngineTests(unittest.TestCase):
    def test_state_fields_exist(self):
        state = build_lunar_state(date(2026, 3, 13))
        self.assertIn(state.element, {"Fire", "Air", "Water", "Earth"})
        self.assertIn(state.day_type, {"Fruit Day", "Flower Day", "Leaf Day", "Root Day"})
        self.assertIn(state.motion, {"Ascending", "Descending"})

    def test_experience_contains_comparison(self):
        experience = build_experience(date(2026, 3, 13), "pair", "curious", "volcanic_red")
        self.assertIn(experience["decision"]["verdict"], {"Open Tonight", "Hold Until Tomorrow", "Split the Difference"})
        self.assertEqual(experience["today"]["date"], "2026-03-13")
        self.assertEqual(experience["tomorrow"]["date"], "2026-03-14")
        self.assertIn("pizza", experience["today"]["table_plan"])
        self.assertIn("claim", experience["proof_lab"])
        self.assertEqual(len(experience["week_horizon"]["nights"]), 7)
        self.assertEqual(experience["selected_bottle_profile"]["key"], "volcanic_red")
        self.assertIsNotNone(experience["today"]["profile_fit"]["score"])

    def test_custom_bottle_profile_round_trip(self):
        custom_bottle = normalize_custom_bottle(
            {
                "custom_name": "Friday fizz",
                "custom_color": "rose",
                "custom_sparkle": "sparkling",
                "custom_body": "light",
                "custom_acid": "5",
                "custom_aroma": "4",
                "custom_savor": "2",
                "custom_fruit": "4",
            }
        )
        experience = build_experience(date(2026, 3, 13), "crowd", "electric", "custom", custom_bottle)
        self.assertEqual(experience["selected_bottle_profile"]["key"], "custom")
        self.assertEqual(experience["custom_bottle"]["name"], "Friday fizz")
        self.assertEqual(experience["custom_bottle"]["sparkle"], "sparkling")
        self.assertIsNotNone(experience["today"]["profile_fit"]["score"])
        self.assertIn("items", experience["today"]["service_map"])

    def test_normalizers_fallback(self):
        self.assertEqual(normalize_party_mode("unknown"), "pair")
        self.assertEqual(normalize_appetite("unknown"), "curious")
        self.assertEqual(normalize_bottle_profile("unknown"), "none")


if __name__ == "__main__":
    unittest.main()
