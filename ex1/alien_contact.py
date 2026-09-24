#!/usr/bin/env python3
"""Alien contact log validation module."""
from __future__ import annotations
from datetime import datetime
from enum import Enum
from pydantic import (
    BaseModel, Field, ValidationError, model_validator
)


class ContactType(str, Enum):
    """Types of contact."""
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    """Alien contact report model with validation rules."""
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode='after')
    def validate_contact_rules(self) -> AlienContact:
        """Validate business rules for alien contact reports."""
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
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )

        if self.signal_strength > 7.0 and not self.message_received:

            raise ValueError(
                "Strong signals (> 7.0) should include received messages"
            )

        return self


def test_valid() -> None:
    """Test creating a valid contact report."""
    try:
        report = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime.now(),
            location="Area 51, Nevada",
            contact_type=ContactType.RADIO,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli",
        )

        print("ID:", report.contact_id)
        print("Type:", report.contact_type.value)
        print("Location:", report.location)
        print(f"Signal: {report.signal_strength}/10")
        print(f"Duration: {report.duration_minutes} minutes")
        print("Witnesses:", report.witness_count)
        print(f"Message: '{report.message_received}'")
    except ValidationError as error:
        for e in error.errors():
            print(e['msg'])


def test_invalid() -> None:
    """Test creating an invalid contact report."""
    try:
        AlienContact(
            contact_id="AC_2024_002",
            timestamp=datetime.now(),
            location="Area 51, Nevada",
            contact_type=ContactType.TELEPATHIC,
            signal_strength=5.0,
            duration_minutes=30,
            witness_count=1,
        )
    except ValidationError as error:
        for e in error.errors():
            msg = e['msg']
            if msg.startswith("Value error, "):
                msg = msg[len("Value error, "):]
            print(msg)


def main() -> None:
    """Demonstration function."""
    print("Alien Contact Log Validation")
    print("======================================")
    print("Valid contact report:")
    test_valid()
    print("======================================")
    print("Expected validation error:")
    test_invalid()


if __name__ == "__main__":
    main()
