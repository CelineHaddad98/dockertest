
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class AddressPost(BaseModel):
    state: str = Field(example='state')
    street: str = Field(example='street')
    license: datetime
    building_number: int = Field(example=4)


class AddressPut(AddressPost):
    created_at: datetime
    updated_at: datetime


class AddressPatch(BaseModel):
    state: Optional[str] = Field(example='state')
    street: Optional[str] = Field(example='street')
    license: Optional[datetime]
    building_number: Optional[int]


class AddressResponse(BaseModel):
    id: UUID 
    state: str
    street: str
    license: datetime
    building_number: int
    created_at: datetime
    updated_at: datetime
