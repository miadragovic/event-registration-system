from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas

from fastapi.responses import StreamingResponse
from io import BytesIO

from blob_utils import upload_file_to_blob, download_blob_to_bytes

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/events/", response_model=schemas.EventRead)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    db_event = models.Event(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.get("/events/", response_model=list[schemas.EventRead])
def read_events(db: Session = Depends(get_db)):
    return db.query(models.Event).all()

@router.post("/registrations/", response_model=schemas.RegistrationRead)
def create_registration(registration: schemas.RegistrationCreate, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == registration.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    db_registration = models.Registration(**registration.model_dump())
    db.add(db_registration)
    db.commit()
    db.refresh(db_registration)
    return db_registration

@router.get("/registrations/", response_model=list[schemas.RegistrationRead])
def read_registrations(db: Session = Depends(get_db)):
    return db.query(models.Registration).all()

# ==== BLOB STORAGE ENDPOINTS ====

@router.post("/blobs/upload/")
async def upload_blob(container: str, file: UploadFile = File(...)):
    file_bytes = await file.read()
    upload_file_to_blob(container, file_bytes, file.filename)
    return {"status": "uploaded", "blob": file.filename}

@router.get("/blobs/download/")
def download_blob(container: str, blob_name: str):
    data = download_blob_to_bytes(container, blob_name)
    return StreamingResponse(BytesIO(data), media_type="application/octet-stream")
