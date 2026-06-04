from datetime import datetime
from typing import Generator
import re

from fastapi import APIRouter, Depends, status
from sqlalchemy import or_, func
from sqlalchemy.orm import Session

from app.db import Knowledge, Memory, SessionLocal
from app.schemas.brain import BrainAsk, BrainChatResponse, BrainProcessRequest, BrainProcessResponse
from app.heart.service import analyze_message
from app.heart.schemas import AnalyzeRequest

router = APIRouter(prefix="/brain", tags=["brain"])


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def build_brain_response(user_message: str) -> str:
    normalized = user_message.strip().lower()

    greetings = {"hello", "hi", "salam"}
    if normalized in greetings:
        return "Hello!"

    if normalized in {"who are you", "what is your name"}:
        return "I am NESLA AI."

    if "time" in normalized:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return "I understand your message but my advanced reasoning module is not connected yet."


def resolve_brain_response(message: str, db: Session) -> str:
    # Normalize and extract simple keywords from the user message
    normalized = message.strip().lower()
    keywords = [k for k in re.findall(r"\w+", normalized) if len(k) > 0]

    if not keywords:
        return build_brain_response(message)

    # Build LIKE conditions for any keyword appearing in title or content
    conditions = []
    for kw in keywords:
        like_pattern = f"%{kw}%"
        conditions.append(func.lower(Knowledge.title).like(like_pattern))
        conditions.append(func.lower(Knowledge.content).like(like_pattern))

    knowledge_entry = (
        db.query(Knowledge)
        .filter(or_(*conditions))
        .order_by(Knowledge.created_at.desc())
        .first()
    )

    if knowledge_entry:
        return knowledge_entry.content

    return build_brain_response(message)


@router.post("/chat", response_model=BrainChatResponse, status_code=status.HTTP_201_CREATED)
def chat_brain(message: BrainAsk, db: Session = Depends(get_db)) -> BrainChatResponse:
    user_message = message.message
    ai_response = resolve_brain_response(user_message, db)
    db_memory = Memory(user_message=user_message, ai_response=ai_response)
    db.add(db_memory)
    db.commit()
    db.refresh(db_memory)
    return BrainChatResponse(
        user_message=user_message,
        response=ai_response,
        timestamp=db_memory.created_at,
    )


@router.post("/ask", response_model=BrainChatResponse, status_code=status.HTTP_201_CREATED)
def ask_brain_endpoint(message: BrainAsk, db: Session = Depends(get_db)) -> BrainChatResponse:
    user_message = message.message
    ai_response = resolve_brain_response(user_message, db)
    db_memory = Memory(user_message=user_message, ai_response=ai_response)
    db.add(db_memory)
    db.commit()
    db.refresh(db_memory)
    return BrainChatResponse(
        user_message=user_message,
        response=ai_response,
        timestamp=db_memory.created_at,
    )


@router.get("/test")
def brain_test() -> dict:
    return {"message": "brain module working"}


def _search_knowledge_for_context(message: str, db: Session) -> str:
    """Search knowledge base for relevant context."""
    normalized = message.strip().lower()
    keywords = [k for k in re.findall(r"\w+", normalized) if len(k) > 0]

    if not keywords:
        return ""

    conditions = []
    for kw in keywords:
        like_pattern = f"%{kw}%"
        conditions.append(func.lower(Knowledge.title).like(like_pattern))
        conditions.append(func.lower(Knowledge.content).like(like_pattern))

    knowledge_entry = (
        db.query(Knowledge)
        .filter(or_(*conditions))
        .order_by(Knowledge.created_at.desc())
        .first()
    )

    return knowledge_entry.content if knowledge_entry else ""


def _search_memory_for_context(message: str, db: Session) -> str:
    """Search memory for relevant past interactions."""
    normalized = message.strip().lower()
    keywords = [k for k in re.findall(r"\w+", normalized) if len(k) > 0]

    if not keywords:
        return ""

    # Simple search: find memories related to similar topics
    recent_memories = db.query(Memory).order_by(Memory.created_at.desc()).limit(5).all()
    for mem in recent_memories:
        for kw in keywords:
            if kw in mem.user_message.lower() or kw in mem.ai_response.lower():
                return f"Similar past: {mem.ai_response}"

    return ""


def _generate_contextual_response(message: str, emotion: str, intent: str, priority: str, db: Session) -> str:
    """Generate response based on emotion, intent, and available context."""
    knowledge_context = _search_knowledge_for_context(message, db)
    memory_context = _search_memory_for_context(message, db)

    # Build response based on emotional context
    if emotion == "sadness":
        base_response = "I understand you're feeling sad. "
    elif emotion == "anger":
        base_response = "I understand you're feeling frustrated. "
    elif emotion == "joy":
        base_response = "Great to hear you're happy! "
    elif emotion == "fear":
        base_response = "I understand you're concerned. "
    else:
        base_response = "Thank you for sharing. "

    # Add context if available
    if knowledge_context:
        base_response += f"Based on our knowledge: {knowledge_context[:100]}... "
    if memory_context:
        base_response += f"Recalling from memory: {memory_context[:100]}... "

    # Handle priority
    if priority == "high":
        base_response += "This appears to be urgent. "

    # Add intent-specific handling
    if intent == "question":
        base_response += "I'm here to help answer your questions."
    elif intent == "request":
        base_response += "I'll do my best to help with your request."
    else:
        base_response += "Thank you for letting me know."

    return base_response


@router.post("/process", response_model=BrainProcessResponse, status_code=status.HTTP_201_CREATED)
def process_with_integration(req: BrainProcessRequest, db: Session = Depends(get_db)) -> BrainProcessResponse:
    """
    Orchestrate all modules: Heart analysis, Knowledge/Memory search, and Mouth response.
    """
    message = req.message

    # Step 1: Analyze with Heart
    heart_analysis = analyze_message(message)
    emotion = heart_analysis.emotion
    intent = heart_analysis.intent
    priority = heart_analysis.priority

    # Step 2 & 3: Search Knowledge and Memory
    # (done inside _generate_contextual_response)

    # Step 4: Generate final response
    final_response = _generate_contextual_response(message, emotion, intent, priority, db)

    # Step 5: Store in Memory
    db_memory = Memory(user_message=message, ai_response=final_response)
    db.add(db_memory)
    db.commit()

    return BrainProcessResponse(
        message=message,
        emotion=emotion,
        intent=intent,
        priority=priority,
        response=final_response,
    )
