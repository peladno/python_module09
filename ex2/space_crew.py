#!/usr/bin/env python3
"""Space crew management module."""
from __future__ import annotations
from datetime import datetime
from enum import Enum
from pydantic import (
    BaseModel, Field, ValidationError, model_validator
)


class Rank(str, Enum):
    """Crew ranks."""
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    """Crew member model."""
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    """Space mission model."""
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def validation_rules(self) -> SpaceMission:
        """Validate safety requirements for space missions."""
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')

        if not any(member.rank in {Rank.CAPTAIN, Rank.COMMANDER}
                   for member in self.crew):
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )

        if self.duration_days > 365:
            experienced = sum(c.years_experience >= 5 for c in self.crew)
            if experienced < len(self.crew) / 2:
                raise ValueError("Long missions (> 365 days) need 50% "
                                 "experienced crew (5+ years)")

        if not all(c.is_active for c in self.crew):
            raise ValueError("All crew members must be active")

        return self


def test_valid_mission() -> None:
    """Test creating a valid space mission."""
    try:
        crew = [
            CrewMember(
                member_id="CM001",
                name="Sarah Connor",
                rank=Rank.COMMANDER,
                age=40,
                specialization="Mission Command",
                years_experience=12,
                is_active=True,
            ),
            CrewMember(
                member_id="CM002",
                name="John Smith",
                rank=Rank.LIEUTENANT,
                age=35,
                specialization="Navigation",
                years_experience=8,
                is_active=True,
            ),
            CrewMember(
                member_id="CM003",
                name="Alice Johnson",
                rank=Rank.OFFICER,
                age=28,
                specialization="Engineering",
                years_experience=3,
                is_active=True,
            ),
        ]

        mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime.now(),
            duration_days=900,
            crew=crew,
            mission_status="planned",
            budget_millions=2500.0,
        )

        print("Mission:", mission.mission_name)
        print("ID:", mission.mission_id)
        print("Destination:", mission.destination)
        print(f"Duration: {mission.duration_days} days")
        print(f"Budget: ${mission.budget_millions}M")
        print("Crew size:", len(mission.crew))
        print("Crew members:")
        for member in mission.crew:
            print(
                f"- {member.name} ({member.rank.value}) - "
                f"{member.specialization}"
            )

    except ValidationError as error:
        for e in error.errors():
            print(e['msg'])


def test_invalid_mission() -> None:
    """Test creating an invalid mission without Commander or Captain."""
    try:
        crew = [
            CrewMember(
                member_id="CM002",
                name="John Smith",
                rank=Rank.LIEUTENANT,
                age=35,
                specialization="Navigation",
                years_experience=8,
                is_active=True,
            ),
            CrewMember(
                member_id="CM003",
                name="Alice Johnson",
                rank=Rank.OFFICER,
                age=28,
                specialization="Engineering",
                years_experience=3,
                is_active=True,
            ),
        ]

        SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime.now(),
            duration_days=900,
            crew=crew,
            mission_status="planned",
            budget_millions=2500.0,
        )

    except ValidationError as error:
        for e in error.errors():
            msg = e['msg']
            if msg.startswith("Value error, "):
                msg = msg[len("Value error, "):]
            print(msg)


def main() -> None:
    """Demonstration function."""
    print("Space Mission Crew Validation")
    print("=========================================")
    print("Valid mission created:")
    test_valid_mission()
    print("=========================================")
    print("Expected validation error:")
    test_invalid_mission()


if __name__ == "__main__":
    main()
