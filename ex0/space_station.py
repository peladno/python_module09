#!/usr/bin/env python3
from pydantic import BaseModel, Field, ValidationError
from datetime import datetime


class SpaceStation(BaseModel):
    """Validation model"""
    station_id: str = Field(..., min_length=1, max_length=30)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.0)
    oxygen_level: float = Field(..., ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: str | None = Field(default=None)


def test_valid() -> None:
    """Testing with correct type data"""
    try:
        station = SpaceStation(
            station_id="1990JP",
            name="Yuki",
            crew_size=20,
            power_level=23.3,
            oxygen_level=100,
            last_maintenance=datetime.now(),
            notes="Today is the day",
            is_operational=False
        )

        print("ID:", station.station_id)
        print("Name:", station.name)
        print(f"Crew size: {station.crew_size} people")
        print(f"Power level: {station.power_level}%")
        print(f"Oxygen level: {station.oxygen_level}%")
        print("Last maintenance:", station.last_maintenance)
        print("Status:", "Operational" if station.is_operational
              else "Non-operational")
        print("Notes:", station.notes)
    except ValidationError as error:
        for e in error.errors():
            print(f"[Error] {e['loc'][0]}:", e['msg'])


def test_invalid() -> None:
    """Test with incorrect type data"""
    try:
        station = SpaceStation(
            station_id="123",
            name="456",
            crew_size=33,
            power_level=23,
            oxygen_level=90,
            last_maintenance=datetime.now()
        )
        print("ID:", station.station_id)
        print("Name:", station.name)
        print(f"Crew size: {station.crew_size} people")
        print(f"Power level: {station.power_level}%")
        print(f"Oxygen level: {station.oxygen_level}%")
        print("Last maintenance:", station.last_maintenance)
        print("Status:", "Operational" if station.is_operational
              else "Non-operational")
    except ValidationError as error:
        for e in error.errors():
            print(f"[Error] {e['loc'][0]}:", e['msg'])


def main() -> None:
    print("Space Station Data Validation")
    print("======================================")
    test_valid()
    print()
    print("======================================")
    print("Expected validation error:")
    test_invalid()


if __name__ == "__main__":
    main()
