from datetime import datetime

from pydantic import BaseModel, Field


class BloodRequestCreate(BaseModel):
    patient_name: str = Field(..., min_length=2, max_length=100)

    blood_group: str = Field(..., min_length=2, max_length=5)

    units_required: int = Field(..., ge=1)

    hospital_name: str = Field(..., min_length=2, max_length=150)

    location: str = Field(..., min_length=2, max_length=100)

    contact_phone: str = Field(..., min_length=10, max_length=20)

    urgency: str = "normal"

    required_date: datetime | None = None

    reason: str | None = None


class BloodRequestUpdate(BaseModel):
    units_required: int | None = Field(None, ge=1)

    hospital_name: str | None = None

    location: str | None = None

    contact_phone: str | None = None

    urgency: str | None = None

    required_date: datetime | None = None

    reason: str | None = None

    status: str | None = None


class BloodRequestResponse(BaseModel):
    id: int

    patient_name: str

    blood_group: str

    units_required: int

    hospital_name: str

    location: str

    contact_phone: str

    urgency: str

    required_date: datetime | None

    reason: str | None

    status: str

    requested_by: int

    created_at: datetime

    class Config:
        from_attributes = True