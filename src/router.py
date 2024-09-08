from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List


from src import schemas
from src import handler
from src.database.db import get_db


router = APIRouter(prefix='/contacts', tags=["contacts"])

@router.post("/", response_model=schemas.ContactResponse)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return handler.create_contact(db, contact)

@router.get("/", response_model=List[schemas.ContactResponse])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return handler.get_contacts(db, skip=skip, limit=limit)

@router.get("/{contact_id}", response_model=schemas.ContactResponse)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = handler.get_contact(db, contact_id)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.put("/{contact_id}", response_model=schemas.ContactResponse)
def update_contact(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(get_db)):
    db_contact = handler.update_contact(db, contact_id, contact)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.delete("/{contact_id}", response_model=schemas.ContactResponse)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = handler.delete_contact(db, contact_id)
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.get("/search", response_model=List[schemas.ContactResponse])
def search_contacts(name: str = None, surname: str = None, email: str = None, db: Session = Depends(get_db)):
    return handler.search_contacts(db, name=name, surname=surname, email=email)

@router.get("/birthdays", response_model=List[schemas.ContactResponse])
def get_upcoming_birthdays(db: Session = Depends(get_db)):
    return handler.get_upcoming_birthdays(db)
