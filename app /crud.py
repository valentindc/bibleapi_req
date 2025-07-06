import httpx
from sqlalchemy.orm import Session
from . import models

BIBLE_API_URL = "https://bible-api.com/"

def get_verse(db: Session, reference: str):
    return db.query(models.Verse).filter(models.Verse.reference == reference).first()

def fetch_verse_from_remote(reference: str) -> dict:
    resp = httpx.get(f"{BIBLE_API_URL}{reference}")
    if resp.status_code == 200:
        return resp.json()
    else:
        resp.raise_for_status()

def create_verse(db: Session, reference: str, text_json: str):
    verse = models.Verse(reference=reference, text=text_json, count=1)
    db.add(verse)
    db.commit()
    db.refresh(verse)
    return verse

def increment_count(db: Session, verse: models.Verse):
    verse.count += 1
    db.commit()
    db.refresh(verse)
    return verse

def get_top_verses(db: Session, limit: int = 3):
    return (
        db.query(models.Verse)
        .order_by(models.Verse.count.desc())
        .limit(limit)
        .all()
    )
