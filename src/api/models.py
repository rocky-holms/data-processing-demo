from typing import Optional

from pydantic import BaseModel, Field, validator


class Record(BaseModel):
    customer_id: int = Field(None, alias="id")
    gender: Optional[str] = Field(None, alias="Gender")
    customer_type: Optional[str] = Field(None, alias="Customer Type")
    age: Optional[int] = Field(None, alias="Age")
    type_of_travel: Optional[str] = Field(None, alias="Type of Travel")
    flight_class: Optional[str] = Field(None, alias="Class")
    flight_distance: Optional[int] = Field(None, alias="Flight Distance")
    inflight_wifi_service: Optional[int] = Field(None, alias="Inflight wifi service")
    departure_and_arrival_time_convenient: Optional[int] = Field(
        None, alias="Departure/Arrival time convenient"
    )
    ease_of_online_booking: Optional[int] = Field(None, alias="Ease of Online booking")
    gate_location: Optional[int] = Field(None, alias="Gate location")
    food_and_drink: Optional[int] = Field(None, alias="Food and drink")
    online_boarding: Optional[int] = Field(None, alias="Online boarding")
    seat_comfort: Optional[int] = Field(None, alias="Seat comfort")
    inflight_entertainment: Optional[int] = Field(None, alias="Inflight entertainment")
    on_board_service: Optional[int] = Field(None, alias="On-board service")
    leg_room_service: Optional[int] = Field(None, alias="Leg room service")
    baggage_handling: Optional[int] = Field(None, alias="Baggage handling")
    check_in_service: Optional[int] = Field(None, alias="Checkin service")
    inflight_service: Optional[int] = Field(None, alias="Inflight service")
    cleanliness: Optional[int] = Field(None, alias="Cleanliness")
    departure_delay_in_minutes: Optional[float] = Field(
        None, alias="Departure Delay in Minutes"
    )
    arrival_delay_in_minutes: Optional[float] = Field(
        None, alias="Arrival Delay in Minutes"
    )
    satisfaction: Optional[str] = Field(None, alias="satisfaction")

    class Config:
        validate_assignment = True

    @validator(
        "inflight_wifi_service",
        "departure_and_arrival_time_convenient",
        "ease_of_online_booking",
        "gate_location",
        "food_and_drink",
        "online_boarding",
        "seat_comfort",
        "inflight_entertainment",
        "on_board_service",
        "leg_room_service",
        "baggage_handling",
        "check_in_service",
        "inflight_service",
        "cleanliness",
    )
    def survey_rate_check(cls, value):
        if value in range(0, 6):
            return value
        else:
            return None

    @validator(
        "age",
        "flight_distance",
        "inflight_wifi_service",
        "departure_and_arrival_time_convenient",
        "ease_of_online_booking",
        "gate_location",
        "food_and_drink",
        "online_boarding",
        "seat_comfort",
        "inflight_entertainment",
        "on_board_service",
        "leg_room_service",
        "baggage_handling",
        "check_in_service",
        "inflight_service",
        "cleanliness",
        pre=True,
    )
    def convert_int_values_check(
        cls,
        value,
    ):
        try:
            new_value = int(value)
            return new_value
        except ValueError:
            return value

    @validator(
        "arrival_delay_in_minutes",
        "departure_delay_in_minutes",
        pre=True,
    )
    def convert_float_values_check(
        cls,
        value,
    ):
        try:
            new_value = float(value)
            return new_value
        except ValueError:
            return value
