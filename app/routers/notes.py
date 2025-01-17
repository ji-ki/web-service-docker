from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Note
from datetime import datetime
from app import models, schemas, database

router = APIRouter()

@router.get("/{note_id}", response_model=schemas.Note, summary="Получить заметку по id", description=":)")
def get_note(note_id: int, db: Session = Depends(database.get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Заметка не найдена")
    return db_note

@router.post("/notes", summary="Создание заметки", description="Просто создать заметку")
def create_note(note: schemas.NoteCreate, db: Session = Depends(database.get_db)):
    if not note.created_at:
        note.created_at = datetime.utcnow()
    db_note = models.Note(title=note.title, content=note.content, created_at=note.created_at)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@router.delete("/{note_id}", tags=["Notes"], summary="Удаление заметки", description="Удалить заметку по ID")
def delete_note(note_id: int, db: Session = Depends(database.get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Заметка не найдена")

    db.delete(db_note)
    db.commit()
    return {"message": "Заметка успешно удалена"}

@router.get("/", response_model=list[schemas.Note], tags=["Notes"], summary="Получить все заметки", description="Возвращает список всех заметок.")
def get_all_notes(db: Session = Depends(database.get_db)):
    notes = db.query(models.Note).all()
    if not notes:
        raise HTTPException(status_code=404, detail="Заметки не найдены")
    return notes