from datetime import datetime
from enum import Enum
from typing import Self
from pydantic import (
    BaseModel, Field, ValidationError, model_validator
    )


class Rank(str, Enum):
    """
    Crew ranks
    """
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=300)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=1000.0)

    @model_validator(mode='after')
    def validation_rules(self) -> Self:
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')

        if not any(member.rank in {Rank.CAPTAIN, Rank.COMMANDER}
                   for member in self.crew):
            raise ValueError("Mission crew must include a "
                             f"{Rank.CAPTAIN.value} or {Rank.COMMANDER.value}")

        if self.duration_days > 365:
            experienced = sum(c.years_experience >= 5 for c in self.crew)
            if experienced < len(self.crew) / 2:
                raise ValueError("Long missions (> 365 days) need 50% "
                                 "experienced crew (5+ years)")

        if not all(c.is_active for c in self.crew):
            raise ValueError("All crew members must be active")

        return self


def test_valid_mission() -> None:
    try:
        crew = [
            CrewMember(
                member_id="CM001",
                name="Alice Johnson",
                rank=Rank.CAPTAIN,
                age=42,
                specialization="Navigation",
                years_experience=15,
                is_active=True
            ),
            CrewMember(
                member_id="CM002",
                name="Bob Smith",
                rank=Rank.OFFICER,
                age=35,
                specialization="Engineering",
                years_experience=10,
                is_active=True
            )
        ]

        mission = SpaceMission(
            mission_id="MSN12345",
            mission_name="Jupiter Exploration",
            destination="Jupiter",
            launch_date=datetime.now(),
            duration_days=540,
            crew=crew,
            mission_status="planned",
            budget_millions=250.5
        )

        print("Valid mission created:")
        print("ID:", mission.mission_id)
        print("Name:", mission.mission_name)
        print("Destination:", mission.destination)
        print("Launch:", mission.launch_date)
        print(f"Duration: {mission.duration_days} days")
        print(f"Budget: ${mission.budget_millions}M")
        print("Status:", mission.mission_status)

        print("Crew Members:")
        for member in mission.crew:
            print(f"- {member.name} ({member.rank.value})")
            print(f"  ID: {member.member_id}")
            print(f"  Age: {member.age}")
            print(f"  Specialization: {member.specialization}")
            print(f"  Experience: {member.years_experience} years")
            print(f"  Active: {member.is_active}")
            print()

    except ValidationError as error:
        for e in error.errors():
            if e['loc']:
                print(f"[Error] {e['loc'][0]}:", e['msg'])
            else:
                print(f"[Error] {list(e['input'])[0]}:",
                      e['msg'].split(",")[1].strip())


def test_invalid_mission() -> None:
    try:
        crew = [
            CrewMember(
                member_id="CM001",
                name="Alice Johnson",
                rank=Rank.OFFICER,
                age=42,
                specialization="Navigation",
                years_experience=1,
                is_active=True
            ),
            CrewMember(
                member_id="CM002",
                name="Bob Smith",
                rank=Rank.OFFICER,
                age=35,
                specialization="Engineering",
                years_experience=1,
                is_active=False
            )
        ]

        mission = SpaceMission(
            mission_id="SN12345",
            mission_name="Jupiter Exploration",
            destination="Jupiter",
            launch_date=datetime.now(),
            duration_days=540,
            crew=crew,
            mission_status="planned",
            budget_millions=250.5
        )

        print("Valid mission created:")
        print("ID:", mission.mission_id)
        print("Name:", mission.mission_name)
        print("Destination:", mission.destination)
        print("Launch:", mission.launch_date)
        print(f"Duration: {mission.duration_days} days")
        print(f"Budget: ${mission.budget_millions}M")
        print("Status:", mission.mission_status)

        print("Crew Members:")
        for member in mission.crew:
            print(f"- {member.name} ({member.rank.value})")
            print(f"  ID: {member.member_id}")
            print(f"  Age: {member.age}")
            print(f"  Specialization: {member.specialization}")
            print(f"  Experience: {member.years_experience} years")
            print(f"  Active: {member.is_active}")
            print()

    except ValidationError as error:
        for e in error.errors():
            if e['loc']:
                print(f"[Error] {e['loc'][0]}:", e['msg'])
            else:
                print(f"[Error] {list(e['input'])[0]}:",
                      e['msg'].split(",")[1].strip())


if __name__ == "__main__":
    print("Space Mission Crew Validation")
    print("=========================================")
    test_valid_mission()
    print("\n=========================================")
    print("Expected validation error:")
    test_invalid_mission()
