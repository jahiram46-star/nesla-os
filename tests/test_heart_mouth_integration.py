import unittest

from Mouth.core.mouth_controller import create_final_speech_package
from Mouth.integrations.heart_connector import HeartConnector


class DummyVoiceProfile:
    def __init__(self) -> None:
        self.average_speed = "slow"
        self.average_pitch = "medium"
        self.average_pause = "high"
        self.average_energy = "calm"


class DummyHeartMemory:
    def get_or_create_voice_profile(self, user_id: str) -> DummyVoiceProfile:
        return DummyVoiceProfile()


class TestHeartMouthIntegration(unittest.TestCase):
    def setUp(self) -> None:
        self.connector = HeartConnector(memory=DummyHeartMemory())

    def test_get_style_profile_returns_valid_profile(self) -> None:
        style_profile = self.connector.get_style_profile("integration_user")

        self.assertEqual(style_profile, {
            "speed": "slow",
            "pitch": "medium",
            "pause": "high",
            "energy": "calm",
        })

    def test_mouth_builds_delivery_profile_from_heart_profile(self) -> None:
        style_profile = self.connector.get_style_profile("integration_user")
        final_package = create_final_speech_package(
            brain_response="আজকে আবহাওয়া ভালো",
            style_profile=style_profile,
        )

        self.assertEqual(final_package, {
            "response_text": "আজকে আবহাওয়া ভালো",
            "speed": "slow",
            "pitch": "medium",
            "pause": "high",
            "energy": "calm",
        })


if __name__ == "__main__":
    unittest.main()
