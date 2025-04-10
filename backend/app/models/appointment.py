from pydantic import BaseModel, UUID4
from typing import Optional, List
from datetime import datetime, date, time

class AppointmentBase(BaseModel):
    date: date
    start_time: time
    end_time: time
    description: Optional[str] = None
    status: str = "scheduled"  # scheduled, completed, cancelled

class AppointmentCreate(AppointmentBase):
    animal_id: UUID4

class AppointmentUpdate(BaseModel):
    date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    description: Optional[str] = None
    status: Optional[str] = None

class AppointmentResponse(AppointmentBase):
    id: UUID4
    clinic_id: UUID4
    animal_id: UUID4
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None 