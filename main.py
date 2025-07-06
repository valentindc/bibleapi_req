from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

# Crear tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bible Verse Service")

# Dependencia para obtener sesión DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/verse/{reference}", response_model=schemas.VerseOut)
def read_verse(reference: str, db: Session = Depends(get_db)):
    # Normalizar la referencia (ej: "john 3:16" → "John 3:16")
    ref_norm = reference.title()
    verse = crud.get_verse(db, ref_norm)
    if verse:
        verse = crud.increment_count(db, verse)
        return {"reference": verse.reference, "text": verse.text}
    # si no existe en cache, fetch remoto
    try:
        text_json = crud.fetch_verse_from_remote(ref_norm)
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=404, detail="Versículo no encontrado")
    verse = crud.create_verse(db, ref_norm, text_json)
    return {"reference": verse.reference, "text": verse.text}

@app.get("/top3", response_model=list[schemas.TopVerse])
def top_three(db: Session = Depends(get_db)):
    top = crud.get_top_verses(db, limit=3)
    return [{"reference": v.reference, "count": v.count} for v in top]
