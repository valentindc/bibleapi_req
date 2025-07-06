from fastapi import FastAPI, HTTPException, Depends, Path
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import LocalSession, engine
import httpx
import json
import re
from .schemas import VerseReference

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bible Verse Service")

# Dependency to get DB session
def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

@app.get("/verse/{reference}", response_model=schemas.VerseOut)
def read_verse(reference: str = Path(..., description="Bible reference (e.g., John 3:16)"), 
               db: Session = Depends(get_db)):
    try:
        # Validate input
        verse_ref = VerseReference(reference=reference)
        ref_norm = verse_ref.reference
        
        # Check local cache first
        verse = crud.get_verse(db, ref_norm)
        if verse:
            verse = crud.increment_count(db, verse)
            # Parse the stored JSON if needed
            if isinstance(verse.text, str):
                verse_data = json.loads(verse.text)
            else:
                verse_data = verse.text
            return {
                "reference": verse.reference,
                "text": verse_data.get("text", ""),
                "translation": verse_data.get("translation")
            }
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e)
        )
    
    try:
        remote_data = crud.fetch_verse_from_remote(ref_norm)
        verse_data = {
            "reference": remote_data.get("reference"),
            "text": remote_data.get("text", ""),
            "translation": remote_data.get("translation_id")
        }
        # Store the structured data
        verse = crud.create_verse(db, ref_norm, json.dumps(verse_data))
        return {
            "reference": verse_data["reference"],
            "text": verse_data["text"],
            "translation": verse_data["translation"]
        }
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Error en API remota")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error procesando respuesta")

@app.get("/top3", response_model=list[schemas.TopVerse])
def top_three(db: Session = Depends(get_db)):
    top = crud.get_top_verses(db, limit=3)
    return [{"reference": v.reference, "count": v.count} for v in top]

@app.get("/health")
def health_check():
    return {"status": "healthy"}