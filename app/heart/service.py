import re
from typing import Tuple

from app.heart.schemas import AnalyzeResponse


def _detect_emotion(message: str) -> str:
    text = message.lower()
    # simple keyword-based emotion detection
    sadness = ["sad", "unhappy", "depressed", "sorrow", "mourn", "lonely"]
    anger = ["angry", "mad", "furious", "annoyed"]
    joy = ["happy", "joy", "glad", "pleased", "excited"]
    fear = ["scared", "afraid", "fear", "terrified", "anxious"]

    for w in sadness:
        if re.search(r"\b" + re.escape(w) + r"\b", text):
            return "sadness"
    for w in anger:
        if re.search(r"\b" + re.escape(w) + r"\b", text):
            return "anger"
    for w in joy:
        if re.search(r"\b" + re.escape(w) + r"\b", text):
            return "joy"
    for w in fear:
        if re.search(r"\b" + re.escape(w) + r"\b", text):
            return "fear"
    return "neutral"


def _detect_intent(message: str) -> str:
    text = message.strip().lower()
    # greeting
    if re.match(r"^(hello|hi|hey|salam)\b", text):
        return "greeting"
    # question detection: ends with ? or starts with wh- words
    if text.endswith("?") or re.match(r"^(what|who|why|how|when|where)\b", text):
        return "question"
    # command/request patterns
    if re.match(r"^(please|can you|could you|i need|i want|need)\b", text) or "please" in text:
        return "request"
    # default to statement
    return "statement"


def _detect_priority(message: str) -> str:
    text = message.lower()
    urgent_words = ["urgent", "immediately", "asap", "emergency", "help me now", "need urgent", "need help now"]
    for w in urgent_words:
        if w in text:
            return "high"
    # phrases indicating higher priority
    if re.search(r"\b(critical|important|important:|priority)\b", text):
        return "high"
    return "normal"


def analyze_message(message: str) -> AnalyzeResponse:
    emotion = _detect_emotion(message)
    intent = _detect_intent(message)
    priority = _detect_priority(message)
    return AnalyzeResponse(emotion=emotion, intent=intent, priority=priority)
