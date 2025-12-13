from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas
from sqlalchemy import text

from fastapi.responses import StreamingResponse
from io import BytesIO

from blob_utils import upload_file_to_blob, download_blob_to_bytes
from auth_utils import get_current_admin, get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/events/", response_model=schemas.EventRead)
def create_event(
    event: schemas.EventCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_admin),  # admin only
):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


@router.get("/events/", response_model=list[schemas.EventRead])
def read_events(db: Session = Depends(get_db)):
    return db.query(models.Event).all()


@router.put("/events/{event_id}", response_model=schemas.EventRead)
def update_event(
    event_id: int,
    event_update: schemas.EventUpdate,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_admin),  # admin only
):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    for field, value in event_update.dict(exclude_unset=True).items():
        setattr(event, field, value)

    db.commit()
    db.refresh(event)
    return event


@router.delete("/events/{event_id}")
def delete_event(
    event_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_admin),  # admin only
):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    db.delete(event)
    db.commit()
    return {"deleted": event_id}



@router.post("/registrations/", response_model=schemas.RegistrationRead)
def create_registration(
    registration: schemas.RegistrationCreate,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user),  # must be logged in
):

    event = db.query(models.Event).filter(models.Event.id == registration.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if event.max_capacity is not None:
        if event.current_count >= event.max_capacity:
            raise HTTPException(status_code=400, detail="Event is full")

    db_registration = models.Registration(**registration.model_dump())
    db.add(db_registration)

    event.current_count += 1

    db.commit()
    db.refresh(db_registration)

    return {
        "id": db_registration.id,
        "event_id": db_registration.event_id,
        "participant_name": db_registration.participant_name,
        "participant_email": db_registration.participant_email,
        "notes": db_registration.notes,
        "event_name": event.name,
        "event_date": event.date.isoformat() if event.date else None,
        "event_location": event.location,
    }


@router.get("/registrations/", response_model=list[schemas.RegistrationRead])
def read_registrations(db: Session = Depends(get_db), email: str = None):
    query = db.query(models.Registration, models.Event).join(
        models.Event, models.Registration.event_id == models.Event.id
    )

    if email:
        query = query.filter(models.Registration.participant_email == email)

    results = query.all()

    output = []
    for reg, ev in results:
        output.append({
            "id": reg.id,
            "event_id": reg.event_id,
            "event_name": ev.name,
            "event_date": ev.date.isoformat() if ev.date else None,
            "event_location": ev.location,
            "participant_name": reg.participant_name,
            "participant_email": reg.participant_email,
            "notes": reg.notes,
            "created_at": reg.created_at.isoformat(),
        })

    return output



@router.delete("/registrations/{reg_id}")
def delete_registration(
    reg_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    reg = db.query(models.Registration).filter(models.Registration.id == reg_id).first()

    if not reg:
        raise HTTPException(status_code=404, detail="Registration not found")

    # Allow only owner or admin
    if reg.participant_email != current_user.email and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not allowed")

    # Decrease event count safely
    event = db.query(models.Event).filter(models.Event.id == reg.event_id).first()
    if event and event.current_count > 0:
        event.current_count -= 1

    db.delete(reg)
    db.commit()

    return {"deleted": reg_id}




@router.post("/blobs/upload/")
async def upload_blob(container: str, file: UploadFile = File(...)):
    file_bytes = await file.read()
    upload_file_to_blob(container, file_bytes, file.filename)
    return {"status": "uploaded", "blob": file.filename}


@router.get("/blobs/download/")
def download_blob(container: str, blob_name: str):
    data = download_blob_to_bytes(container, blob_name)
    return StreamingResponse(BytesIO(data), media_type="application/octet-stream")



@router.get("/health/db")
def db_health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {e}")
