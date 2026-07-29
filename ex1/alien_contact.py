#!/usr/bin/env python3
from pydantic import BaseModel, Field, model_validator
from enum import Enum
from datetime import datetime


class ContactType(str, Enum):
    """
    Types of contact
    """
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(max_length=3, max_digits=100)
    contact_type: ContactType
    signal_strenght: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_recieved: str | None = Field(max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode='after')
        