from pydantic import BaseModel


class LocationQuery(BaseModel):
    term: str
    locale: str = "en-US"
    location_types: str = "city"
    limit: int = 5

