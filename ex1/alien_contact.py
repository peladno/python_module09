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
    location: str = Field(min_length=3, max_length=100)
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
            raise ValueError(f"{ContactType.TELEPATHIC.value} "
                             "contact requires "
                             "at least 3 witnesses")
        # testear esto
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

        print("ID:", alien_contact.contact_id)
        print("Type:", alien_contact.contact_type.value)
        print("Location:", alien_contact.location)
        print(f"Signal: {alien_contact.signal_strenght}/10")
        print(f"Duration: {alien_contact.duration_minutes} minutes")
        print("Witnesses:", alien_contact.witness_count)
        print("Message:", alien_contact.message_recieved)

    except ValidationError as error:
        for e in error.errors():
            if e['loc']:
                print(f"[Error] {e['loc'][0]}:", e['msg'])
            else:
                print(f"[Error] {list(e['input'])[0]}:",
                      e['msg'].split(",")[1].strip())


def test_invalid() -> None:
    try:
        alien_contact = AlienContact(
            contact_id="AC4242dd",
            timestamp=datetime.now(),
            location="Tokyo",
            contact_type=ContactType.TELEPATHIC,
            duration_minutes=30,
            signal_strenght=7.2,
            witness_count=2,
            message_recieved="OMG",
            is_verified=True
        )

        print("ID:", alien_contact.contact_id)
        print("Type:", alien_contact.contact_type.value)
        print("Location:", alien_contact.location)
        print(f"Signal: {alien_contact.signal_strenght}/10")
        print(f"Duration: {alien_contact.duration_minutes} minutes")
        print("Witnesses:", alien_contact.witness_count)
        print("Message:", alien_contact.message_recieved)

    except ValidationError as error:
        for e in error.errors():
            if e['loc']:
                print(f"[Error] {e['loc'][0]}:", e['msg'])
            else:
                print(f"[Error] {list(e['input'])[0]}:",
                      e['msg'].split(",")[1].strip())


if __name__ == "__main__":
    print("Alien Contact Log Validation")
    print("=======================================")
    print("Valid contact report:")
    test_valid()
    print("\n=======================================")
    print("Invalid contact report:")
    test_invalid()
