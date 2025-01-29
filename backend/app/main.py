from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import os
import requests
from .database import SessionLocal, engine, Base
from .models import TarotCard, UserSession
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ReadingRequest(BaseModel):
    question: str
    selected_cards: List[int]
    user_name: str
    dob: str
    gender: str

@app.post("/api/reading")
async def create_reading(request: ReadingRequest, db: Session = Depends(get_db)):
    # Save user session
    session = UserSession(
        name=request.user_name,
        dob=request.dob,
        gender=request.gender,
        question=request.question
    )
    db.add(session)
    db.commit()

    # Get card meanings
    cards = db.query(TarotCard).filter(TarotCard.id.in_(request.selected_cards)).all()

    # Call OpenRouter API
    openrouter_url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }

    prompt = f"Provide a tarot reading for: {request.question} using these cards: {[card.name for card in cards]}"

    try:
        payload = {
            "model": "google/palm-2", # or try "openai/gpt-3.5-turbo"
            "messages": [{"role": "user", "content": prompt}]
        }

        response = requests.post(openrouter_url, json=payload, headers=headers)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        interpretation = response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"LLM API Error: {str(e)}")
    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"LLM Response Parsing Error: {str(e)}")


    return {
        "interpretation": interpretation,
        "cards": [card.__dict__ for card in cards]
    }

@app.get("/api/cards")
async def get_cards(db: Session = Depends(get_db)):
    return db.query(TarotCard).all()

@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    if not db.query(TarotCard).first():
        cards_data = [
            {"id": 1, "name": "The Fool", "image_url": "/images/fool.jpg", "meaning_upright": "New beginnings, innocence, adventure.", "meaning_reversed": "Naivety, recklessness, holding back."},
            {"id": 2, "name": "The Magician", "image_url": "/images/magician.jpg", "meaning_upright": "Willpower, skill, concentration, resourcefulness.", "meaning_reversed": "Manipulation, poor planning, untapped talents."},
            {"id": 3, "name": "The High Priestess", "image_url": "/images/highpriestess.jpg", "meaning_upright": "Intuition, mystery, wisdom, serenity.", "meaning_reversed": "Secrets, silence, listening to the wrong voice."},
            {"id": 4, "name": "The Empress", "image_url": "/images/empress.jpg", "meaning_upright": "Abundance, nature, fertility, life.", "meaning_reversed": "Dependence, smothering, lack of growth."},
            {"id": 5, "name": "The Emperor", "image_url": "/images/emperor.jpg", "meaning_upright": "Authority, structure, control, fatherhood.", "meaning_reversed": "Tyranny, rigidity, lack of discipline."},
            {"id": 6, "name": "The Hierophant", "image_url": "/images/hierophant.jpg", "meaning_upright": "Tradition, conformity, morality, ethics.", "meaning_reversed": "Rebellion, unconventionality, new approaches."},
            {"id": 7, "name": "The Lovers", "image_url": "/images/lovers.jpg", "meaning_upright": "Love, harmony, choices, relationships.", "meaning_reversed": "Disharmony, imbalance, bad choices."},
            {"id": 8, "name": "The Chariot", "image_url": "/images/chariot.jpg", "meaning_upright": "Willpower, direction, control, victory.", "meaning_reversed": "Lack of control, lack of direction, defeat."},
            {"id": 9, "name": "Strength", "image_url": "/images/strength.jpg", "meaning_upright": "Courage, patience, compassion, focus.", "meaning_reversed": "Self-doubt, weakness, insecurity."},
            {"id": 10, "name": "The Hermit", "image_url": "/images/hermit.jpg", "meaning_upright": "Introspection, solitude, guidance, inner wisdom.", "meaning_reversed": "Isolation, loneliness, withdrawal."},
            {"id": 11, "name": "Wheel of Fortune", "image_url": "/images/wheeloffortune.jpg", "meaning_upright": "Change, cycles, destiny, luck.", "meaning_reversed": "Bad luck, negative cycles, lack of control."},
            {"id": 12, "name": "Justice", "image_url": "/images/justice.jpg", "meaning_upright": "Fairness, truth, balance, law.", "meaning_reversed": "Injustice, unfairness, imbalance."},
            {"id": 13, "name": "The Hanged Man", "image_url": "/images/hangedman.jpg", "meaning_upright": "Sacrifice, release, new perspective, suspension.", "meaning_reversed": "Stalling, fear of sacrifice, useless sacrifice."},
            {"id": 14, "name": "Death", "image_url": "/images/death.jpg", "meaning_upright": "Endings, beginnings, change, transformation.", "meaning_reversed": "Fear of change, holding on, decay."},
            {"id": 15, "name": "Temperance", "image_url": "/images/temperance.jpg", "meaning_upright": "Balance, moderation, patience, harmony.", "meaning_reversed": "Imbalance, excess, lack of long-term vision."},
            {"id": 16, "name": "The Devil", "image_url": "/images/devil.jpg", "meaning_upright": "Materialism, addiction, temptation, shadow self.", "meaning_reversed": "Breaking free, reclaiming power, facing fears."},
            {"id": 17, "name": "The Tower", "image_url": "/images/tower.jpg", "meaning_upright": "Sudden change, upheaval, chaos, revelation.", "meaning_reversed": "Resistance to change, delaying the inevitable."},
            {"id": 18, "name": "The Star", "image_url": "/images/star.jpg", "meaning_upright": "Hope, inspiration, serenity, faith.", "meaning_reversed": "Despair, lack of faith, negativity."},
            {"id": 19, "name": "The Moon", "image_url": "/images/moon.jpg", "meaning_upright": "Intuition, dreams, the subconscious, illusion.", "meaning_reversed": "Confusion, fear, deception, misinterpretation."},
            {"id": 20, "name": "The Sun", "image_url": "/images/sun.jpg", "meaning_upright": "Joy, success, energy, clarity, positivity.", "meaning_reversed": "Negativity, sadness, lack of clarity, blocked energy."},
            {"id": 21, "name": "Judgement", "image_url": "/images/judgement.jpg", "meaning_upright": "Reflection, reckoning, awakening, renewal.", "meaning_reversed": "Self-doubt, denial, fear of judgement."},
            {"id": 22, "name": "The World", "image_url": "/images/world.jpg", "meaning_upright": "Completion, achievement, travel, wholeness.", "meaning_reversed": "Incompletion, delays, lack of closure."}
        ]
        for card_data in cards_data:
            card = TarotCard(**card_data)
            db.add(card)
        db.commit()
    db.close()
