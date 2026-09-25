from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user
from models import BloodRequest, User
from schemas.blood_request import BloodRequestCreate,BloodRequestResponse,BloodRequestUpdate

router = APIRouter(prefix="/blood-requests",tags=["Blood Requests"])


@router.post("/",response_model=BloodRequestResponse)
def create_blood_request(request_data: BloodRequestCreate,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):

    new_request = BloodRequest(
        patient_name=request_data.patient_name,
        blood_group=request_data.blood_group,
        units_required=request_data.units_required,
        hospital_name=request_data.hospital_name,
        location=request_data.location,
        contact_phone=request_data.contact_phone,
        urgency=request_data.urgency,
        required_date=request_data.required_date,
        reason=request_data.reason,
        requested_by=current_user.id
    )

    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return new_request


@router.get("/",response_model=list[BloodRequestResponse])
def get_blood_requests(
    search: str | None = None,
    request_id: int | None = None,
    blood_group: str | None = None,
    location: str | None = None,
    status: str | None = None,
    urgency: str | None = None,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    sort: str = "newest",
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(BloodRequest)

    if search:
        query = query.filter(BloodRequest.patient_name.ilike(f"%{search}%"))

    if request_id is not None:
        query = query.filter(BloodRequest.id == request_id)

    if blood_group:
        query = query.filter(BloodRequest.blood_group == blood_group)

    if location:
        query = query.filter(BloodRequest.location.ilike(f"%{location}%"))

    if status:
        query = query.filter(BloodRequest.status == status)

    if urgency:
        query = query.filter(BloodRequest.urgency == urgency)

    if start_date:
        query = query.filter(BloodRequest.created_at >= start_date)

    if end_date:
        query = query.filter(BloodRequest.created_at <= end_date)

    if sort == "newest":
        query = query.order_by(BloodRequest.created_at.desc())

    elif sort == "oldest":
        query = query.order_by(BloodRequest.created_at.asc())

    elif sort == "name_asc":
        query = query.order_by(BloodRequest.patient_name.asc())

    elif sort == "name_desc":
        query = query.order_by(BloodRequest.patient_name.desc())

    elif sort == "date_asc":
        query = query.order_by(BloodRequest.required_date.asc())

    elif sort == "date_desc":
        query = query.order_by(BloodRequest.required_date.desc())

    return query.offset(skip).limit(limit).all()


@router.get("/me",response_model=list[BloodRequestResponse])
def get_my_requests(current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):

    return db.query(BloodRequest).filter(BloodRequest.requested_by == current_user.id).all()


@router.get("/{request_id}",response_model=BloodRequestResponse)
def get_blood_request(request_id: int,db: Session = Depends(get_db)):

    request = db.query(BloodRequest).filter(BloodRequest.id == request_id).first()

    if not request:
        raise HTTPException(status_code=404,detail="Blood request not found")
    return request


@router.put("/{request_id}",response_model=BloodRequestResponse)
def update_blood_request(request_id: int,request_data: BloodRequestUpdate,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):

    request = db.query(BloodRequest).filter(BloodRequest.id == request_id).first()

    if not request:
        raise HTTPException(status_code=404,detail="Blood request not found")

    if (request.requested_by != current_user.id and current_user.role != "admin"):

        raise HTTPException(status_code=403,detail="You cannot update this request")

    update_data = request_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(request, key, value)

    db.commit()
    db.refresh(request)

    return request


@router.delete("/{request_id}")
def delete_blood_request(request_id: int,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):

    request = db.query(BloodRequest).filter(BloodRequest.id == request_id).first()

    if not request:
        raise HTTPException(status_code=404,detail="Blood request not found")

    if (request.requested_by != current_user.id and current_user.role != "admin"):

        raise HTTPException(status_code=403,detail="You cannot delete this request")

    db.delete(request)
    db.commit()

    return {"message": "Blood request deleted successfully"}
