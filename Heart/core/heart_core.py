from typing import Any, Dict

from Heart.analyzers.emotion_analyzer import EmotionAnalyzer
from Heart.analyzers.rhythm_analyzer import RhythmAnalyzer
from Heart.analyzers.tone_analyzer import ToneAnalyzer
from Heart.composer.voice_style_composer import VoiceStyleComposer
from Heart.core.profile_manager import VoiceProfileManager
from Heart.core.musical_engine import MusicalEngine
from Heart.controllers.energy_controller import EnergyController
from Heart.controllers.pause_controller import PauseController
from Heart.controllers.pitch_controller import PitchController
from Heart.learner.user_style_learner import UserStyleLearner
from Heart.memory.heart_memory import HeartMemory


class HeartCore:
    """Heart V2 orchestration layer.

    Heart receives original voice input + user ID, then learns speaking patterns
    and produces a delivery profile for Mouth.
    """

    def __init__(self) -> None:
        self.emotion_analyzer = EmotionAnalyzer()
        self.tone_analyzer = ToneAnalyzer()
        self.rhythm_analyzer = RhythmAnalyzer()
        self.user_style_learner = UserStyleLearner()
        self.profile_manager = VoiceProfileManager()
        self.musical_engine = MusicalEngine()
        self.pitch_controller = PitchController()
        self.pause_controller = PauseController()
        self.energy_controller = EnergyController()
        self.memory = HeartMemory()
        self.composer = VoiceStyleComposer()

    def process_voice(self, user_id: str, original_voice: Dict[str, Any]) -> Dict[str, Any]:
        """Process one voice event and update Heart learning state."""
        voice_profile = self.memory.get_or_create_voice_profile(user_id)

        emotion = self.emotion_analyzer.analyze(original_voice)
        tone = self.tone_analyzer.analyze(original_voice)
        rhythm = self.rhythm_analyzer.analyze(original_voice)

        learning_metrics = self.user_style_learner.learn(
            user_id=user_id,
            voice_payload=original_voice,
            emotion=emotion,
            tone=tone,
            rhythm=rhythm,
        )

        style = self.composer.build_style_profile(
            speed=learning_metrics["speed"],
            pitch=self.pitch_controller.select_pitch(learning_metrics["pitch"], tone, emotion),
            pause=self.pause_controller.select_pause(learning_metrics["pause"], rhythm),
            energy=self.energy_controller.select_energy(learning_metrics["energy"], emotion, tone),
        )

        updated_profile = self.profile_manager.update_profile(
            user_id=user_id,
            base_profile=voice_profile,
            new_style=style,
            sample_count=self.memory.get_sample_count(user_id),
        )
        self.memory.save_voice_profile(updated_profile)

        musical_descriptor = self.musical_engine.compose(self.composer.serialize(style))

        return {
            "style_profile": self.composer.serialize(style),
            "musical_descriptor": musical_descriptor,
            "learned_metrics": learning_metrics,
        }
