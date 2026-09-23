from datetime import datetime
from pydantic import BaseModel


class DonationCreate(BaseModel):
    blood_request_id: int
    notes: str | None = None


class DonationUpdate(BaseModel):
    status: str | None = None
    donation_date: datetime | None = None
    notes: str | None = None


class DonationResponse(BaseModel):
    id: int

    donor_id: int

    blood_request_id: int

    donation_date: datetime | None

    status: str

    notes: str | None

    created_at: datetime

    class Config:
        from_attributes = True