from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from src.database import models
from src import schemas


def get_contact(db: Session, contact_id: int):
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()

def get_contacts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Contact).offset(skip).limit(limit).all()

def create_contact(db: Session, contact: schemas.ContactCreate):
    db_contact = models.Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(db: Session, contact_id: int, contact: schemas.ContactUpdate):
    db_contact = get_contact(db, contact_id)
    if db_contact:
        for key, value in contact.model_dump(exclude_unset=True).items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int):
    db_contact = get_contact(db, contact_id)
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact


def search_contacts(db: Session, name: str = None, surname: str = None, email: str = None):
    query = db.query(models.Contact)
    if name:
        query = query.filter(models.Contact.name.ilike(f"%{name}%"))
    if surname:
        query = query.filter(models.Contact.surname.ilike(f"%{surname}%"))
    if email:
        query = query.filter(models.Contact.email.ilike(f"%{email}%"))
    return query.all()

def get_upcoming_birthdays(db: Session):
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    return db.query(models.Contact).filter(
        func.date_trunc('day', models.Contact.birth_date) >= today,
        func.date_trunc('day', models.Contact.birth_date) <= next_week
    ).all()
