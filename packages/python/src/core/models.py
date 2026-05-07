from enum import Enum
from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class RecurrencyType(str, Enum):
    daily = 'daily'
    weekly = 'weekly'
    biweekly = 'biweekly'
    monthly = 'monthly'
    custom_days = 'custom_days'

class RegisterType(str, Enum):
    event = 'event'
    schedule = 'schedule'

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    image: Optional[str] = None
    note: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: UUID
    creation_date_time: datetime
    update_date_time: datetime
    model_config = ConfigDict(from_attributes=True)

class ScheduledRoutineBase(BaseModel):
    name: str
    category_id: Optional[UUID] = None
    start_date_time: datetime
    end_date_time: datetime
    description: Optional[str] = None
    note: Optional[str] = None
    recurrency: RecurrencyType

class ScheduledRoutineCreate(ScheduledRoutineBase):
    pass

class ScheduledRoutine(ScheduledRoutineBase):
    id: UUID
    creation_date_time: datetime
    update_date_time: datetime
    model_config = ConfigDict(from_attributes=True)

class DateRegisterBase(BaseModel):
    type: RegisterType
    name: str
    start_date_time: datetime
    end_date_time: datetime
    description: Optional[str] = None
    note: Optional[str] = None
    category_id: Optional[UUID] = None
    scheduled_routine_id: Optional[UUID] = None
    relationship_field: Optional[str] = None

class DateRegisterCreate(DateRegisterBase):
    pass

class DateRegister(DateRegisterBase):
    id: UUID
    creation_date_time: datetime
    update_date_time: datetime
    model_config = ConfigDict(from_attributes=True)
