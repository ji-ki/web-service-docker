from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app import models, schemas, database

router = APIRouter()


@router.get("/{note_id}", response_model=schemas.Note)
def get_note(note_id: int, db: Session = Depends(database.get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Заметка не найдена")
    return db_note

@router.put("/{note_id}", response_model=schemas.Note)
def update_note(note_id: int, updated_note: schemas.NoteCreate, db: Session = Depends(database.get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Заметка не найдена")

    db_note.title = updated_note.title
    db_note.content = updated_note.content
    db_note.created_at = updated_note.created_at 

    db.commit()
    db.refresh(db_note)
    return db_note

@router.delete("/{note_id}", tags=["Notes"])
def delete_note(note_id: int, db: Session = Depends(database.get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if db_note is None:
        raise HTTPException(status_code=404, detail="Заметка не найдена")

    db.delete(db_note)
    db.commit()
    return {"сообщение": "Заметка успешно удалена"}

