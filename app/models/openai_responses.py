from pydantic import BaseModel


class DestinationResponse(BaseModel):
    reasoning: str
    airport_codes: list[str]


class TimeParamsResponse(BaseModel):
    departure_date_from: str
    departure_date_to: str
    nights_in_dst_from: int | None = None
    nights_in_dst_to: int | None = None
    fly_days: list[int] | None = None
    ret_fly_days: list[int] | None = None
    fly_days_type: str | None = None
    ret_fly_days_type: str | None = None


class DurationParamsResponse(BaseModel):
    reasoning: str
    max_sector_stopovers: int | None = None
    stopover_to: str | None = None
    max_fly_duration: int | None = None
