from pydantic import BaseModel


class Travelers(BaseModel):
    adults: int = 1
    children: int = 0
    infants: int = 0


class FlightRequest(BaseModel):
    user_request: str
    selected_city_id: str
    cabin_class: str = "M"
    travelers: Travelers

