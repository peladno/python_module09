#!/usr/bin/env python3
from pydantic import BaseModel, Field, ValidationError, model_validator
from enum import Enum
from datetime import datetime
from typing_extensions import Self


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
    def check_to_Validate(self) -> Self:
        if not self.contact_id.startswith("AC"):
            raise ValueError('Contact ID must start with "AC"')

        if (
            self.contact_type == ContactType.PHYSICAL
            and not self.is_verified
        ):
            raise ValueError("Physical contact reports must be verified")

        if (
            self.contact_type == ContactType.TELEPATHIC
            and self.witness_count < 3
        ):
            raise ValueError("Telepathic contact requires "
                             "at least 3 witnesses")
        if not self.message_recieved and self.signal_strenght <= 7.0:
            raise ValueError("Strong signals (> 7.0) should include "
                             "received messages")

        return self


def test_valid() -> None:
    try:
        alien_contact = AlienContact(
            contact_id="AC4242",
            timestamp=datetime.now(),
            location="Tokyo",
            contact_type=ContactType.PHYSICAL,
            duration_minutes=30,
            signal_strenght=7.2,
            witness_count=4,
            message_recieved="OMG",
            is_verified=True
        )

        print("Valid contact report:")
        print("ID", alien_contact.contact_id)
    except ValidationError as error:
        for e in error.errors():
            print(f"[Error] {e['loc'][0]}:", e['msg'])
