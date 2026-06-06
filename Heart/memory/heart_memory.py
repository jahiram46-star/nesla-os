from typing import Any, Dict, Optional

from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import Session

from app.db.database import Base, SessionLocal


class UserVoiceProfile(Base):
    __tablename__ = "user_voice_profiles"

    user_id = Column(String(length=128), primary_key=True, index=True)
    average_speed = Column(Float, nullable=False, default=1.0)
    average_pitch = Column(String(length=32), nullable=False, default="medium")
    average_pause = Column(String(length=32), nullable=False, default="low")
    average_energy = Column(String(length=32), nullable=False, default="medium")
    confidence_score = Column(Float, nullable=False, default=0.0)
    sample_count = Column(Integer, nullable=False, default=0)


class EmotionHistory(Base):
    __tablename__ = "emotion_history"

    user_id = Column(String(length=128), primary_key=True, index=True)
    happy_count = Column(Integer, nullable=False, default=0)
    sad_count = Column(Integer, nullable=False, default=0)
    calm_count = Column(Integer, nullable=False, default=0)
    excited_count = Column(Integer, nullable=False, default=0)
    angry_count = Column(Integer, nullable=False, default=0)


class RhythmHistory(Base):
    __tablename__ = "rhythm_history"

    user_id = Column(String(length=128), primary_key=True, index=True)
    fast_count = Column(Integer, nullable=False, default=0)
    medium_count = Column(Integer, nullable=False, default=0)
    slow_count = Column(Integer, nullable=False, default=0)


class ToneHistory(Base):
    __tablename__ = "tone_history"

    user_id = Column(String(length=128), primary_key=True, index=True)
    friendly_count = Column(Integer, nullable=False, default=0)
    formal_count = Column(Integer, nullable=False, default=0)
    professional_count = Column(Integer, nullable=False, default=0)


class StyleProfiles(Base):
    __tablename__ = "style_profiles"

    profile_name = Column(String(length=128), primary_key=True, index=True)
    speed = Column(Float, nullable=False, default=1.0)
    pitch = Column(String(length=32), nullable=False, default="medium")
    pause = Column(String(length=32), nullable=False, default="low")
    energy = Column(String(length=32), nullable=False, default="medium")
    confidence = Column(Float, nullable=False, default=0.0)


class HeartMemory:
    """Persistence layer for Heart V2 profiles and historical patterns."""

    def __init__(self) -> None:
        self.session_factory = SessionLocal

    def _get_session(self) -> Session:
        return self.session_factory()

    def get_or_create_voice_profile(self, user_id: str) -> UserVoiceProfile:
        session = self._get_session()
        try:
            profile = session.get(UserVoiceProfile, user_id)
            if profile is None:
                profile = UserVoiceProfile(user_id=user_id)
                session.add(profile)
                session.commit()
                session.refresh(profile)
            return profile
        finally:
            session.close()

    def save_voice_profile(self, profile: UserVoiceProfile) -> None:
        session = self._get_session()
        try:
            existing = session.get(UserVoiceProfile, profile.user_id)
            if existing is None:
                session.add(profile)
            else:
                existing.average_speed = profile.average_speed
                existing.average_pitch = profile.average_pitch
                existing.average_pause = profile.average_pause
                existing.average_energy = profile.average_energy
                existing.confidence_score = profile.confidence_score
                existing.sample_count = profile.sample_count
            session.commit()
        finally:
            session.close()

    def record_voice_sample(self, user_id: str) -> None:
        profile = self.get_or_create_voice_profile(user_id)
        profile.sample_count = profile.sample_count + 1
        session = self._get_session()
        try:
            existing = session.get(UserVoiceProfile, user_id)
            if existing is None:
                session.add(profile)
            else:
                existing.sample_count = profile.sample_count
            session.commit()
        finally:
            session.close()

    def record_emotion(self, user_id: str, emotion: str) -> None:
        self._increment_counter(EmotionHistory, user_id, emotion)

    def record_rhythm(self, user_id: str, rhythm: str) -> None:
        self._increment_counter(RhythmHistory, user_id, rhythm)

    def record_tone(self, user_id: str, tone: str) -> None:
        self._increment_counter(ToneHistory, user_id, tone)

    def get_sample_count(self, user_id: str) -> int:
        profile = self.get_or_create_voice_profile(user_id)
        return profile.sample_count

    def _increment_counter(self, model: Any, user_id: str, label: str) -> None:
        session = self._get_session()
        try:
            record = session.get(model, user_id)
            if record is None:
                record = model(user_id=user_id)
                session.add(record)
            key = self._label_to_field(label)
            if hasattr(record, key):
                current = getattr(record, key, 0) or 0
                setattr(record, key, current + 1)
            session.commit()
        finally:
            session.close()

    @staticmethod
    def _label_to_field(label: str) -> str:
        mapping = {
            "happy": "happy_count",
            "sad": "sad_count",
            "calm": "calm_count",
            "excited": "excited_count",
            "angry": "angry_count",
            "fast": "fast_count",
            "medium": "medium_count",
            "slow": "slow_count",
            "friendly": "friendly_count",
            "formal": "formal_count",
            "professional": "professional_count",
        }
        return mapping.get(label, "medium_count")
