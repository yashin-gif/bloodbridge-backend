from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user
from models import BloodRequest, Donation, User
from schemas.donation import DonationCreate,DonationResponse,DonationUpdate

router = APIRouter(prefix="/donations",tags=["Donations"])

@router.post("/",response_model=DonationResponse)
def create_donation(donation_data: DonationCreate,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):

    blood_request = db.query(BloodRequest).filter(BloodRequest.id == donation_data.blood_request_id).first()

    if not blood_request:
        raise HTTPException(status_code=404,detail="Blood request not found")

    if blood_request.requested_by == current_user.id:
        raise HTTPException(status_code=400,detail="You cannot donate to your own blood request")

    existing_donation = db.query(Donation).filter(Donation.donor_id == current_user.id,Donation.blood_request_id == donation_data.blood_request_id).first()

    if existing_donation:
        raise HTTPException(status_code=400,detail="You have already submitted a donation for this blood request")

    new_donation = Donation(donor_id=current_user.id,blood_request_id=donation_data.blood_request_id,notes=donation_data.notes)

    db.add(new_donation)
    db.commit()
    db.refresh(new_donation)

    return new_donation

@router.get("/me",response_model=list[DonationResponse])
def get_my_donations(current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):

    return db.query(Donation).filter(Donation.donor_id == current_user.id).all()


@router.get("/",response_model=list[DonationResponse])
def get_donations(skip: int = 0,limit: int = 10,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):

    if current_user.role != "admin":
        raise HTTPException(status_code=403,detail="Admin access required")

    return db.query(Donation).offset(skip).limit(limit).all()

@router.put("/{donation_id}",response_model=DonationResponse)
def update_donation(donation_id: int,donation_data: DonationUpdate,current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):

    donation = db.query(Donation).filter(Donation.id == donation_id).first()

    if not donation:
        raise HTTPException(status_code=404,detail="Donation not found")

    if(
        donation.donor_id != current_user.id
        and current_user.role != "admin"
    ):
        raise HTTPException(status_code=403,detail="You cannot update this donation")

    update_data = donation_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(donation, key, value)
    db.commit()
    db.refresh(donation)

    return donation