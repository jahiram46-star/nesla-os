import unittest

from Mouth.core.mouth_controller import create_final_speech_package
from Mouth.core.delivery_profile_builder import build_delivery_profile


class TestMouthV2Core(unittest.TestCase):
    def test_build_delivery_profile_uses_style_profile_values(self) -> None:
        delivery_profile = build_delivery_profile(
            brain_response="Hello from Brain.",
            style_profile={
                "speed": "fast",
                "pitch": "medium",
                "pause": "low",
                "energy": "high",
            },
        )

        self.assertEqual(delivery_profile, {
            "response_text": "Hello from Brain.",
            "speed": "fast",
            "pitch": "medium",
            "pause": "low",
            "energy": "high",
        })

    def test_build_delivery_profile_falls_back_to_defaults(self) -> None:
        delivery_profile = build_delivery_profile(
            brain_response="Fallback response.",
            style_profile={"speed": 1.3},
        )

        self.assertEqual(delivery_profile["response_text"], "Fallback response.")
        self.assertEqual(delivery_profile["speed"], 1.3)
        self.assertEqual(delivery_profile["pitch"], "medium")
        self.assertEqual(delivery_profile["pause"], "normal")
        self.assertEqual(delivery_profile["energy"], "normal")

    def test_create_final_speech_package_returns_final_package(self) -> None:
        final_package = create_final_speech_package(
            brain_response="Final answer.",
            style_profile={
                "speed": "slow",
                "pitch": "high",
                "pause": "medium",
                "energy": "low",
            },
        )

        self.assertEqual(final_package, {
            "response_text": "Final answer.",
            "speed": "slow",
            "pitch": "high",
            "pause": "medium",
            "energy": "low",
        })
