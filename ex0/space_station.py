#!/usr/bin/env python3
from pydantic import BaseModel, Field, ValidationError
from datetime import datetime


class SpaceStation(BaseModel):
    """Validation model"""
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: str | None = Field(default=None, max_length=200)


def test_valid() -> None:
    """Testing with correct type data"""
    try:
        station = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime.now(),
        )

        print("ID:", station.station_id)
        print("Name:", station.name)
        print(f"Crew: {station.crew_size} people")
        print(f"Power: {station.power_level}%")
        print(f"Oxygen: {station.oxygen_level}%")
        print(
            "Status:",
            "Operational" if station.is_operational else "Non-operational",
        )
    except ValidationError as error:
        for e in error.errors():
            print(f"[Error] {e['loc'][0]}:", e['msg'])


def test_invalid() -> None:
    """Testing with incorrect type data"""
    try:
        SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=25,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime.now(),
        )
    except ValidationError as error:
        for e in error.errors():
            print(e['msg'])


def main() -> None:
    """Demonstration function"""
    print("Space Station Data Validation")
    print("========================================")
    print("Valid station created:")
    test_valid()
    print("========================================")
    print("Expected validation error:")
    test_invalid()


if __name__ == "__main__":
    main()
