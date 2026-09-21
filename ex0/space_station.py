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
            station_id="1990JP",
            name="Yuki",
            crew_size=20,
            power_level=23.3,
            oxygen_level=100,
            last_maintenance=datetime.now(),
            notes="Lorem ipsum dolor sit amet, "
            "consectetuer adipiscing elit. Aenean "
            "commodo ligula eget dolor. Aenean massa. "
            "Cum sociis natoque penatibus et magnis dis "
            "parturient montes, nascetur ridiculus mus. Donec qu",
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


def main() -> None:
    print("Space Station Data Validation")
    print("======================================")
    test_valid()
    print()


if __name__ == "__main__":
    main()
