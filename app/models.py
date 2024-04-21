from pydantic import BaseModel, HttpUrl, ValidationError
from pydantic.functional_validators import field_validator

class Product(BaseModel):
    title: str
    price: float
    image_url: HttpUrl

    @field_validator('image_url')
    def convert_url_to_string(cls, v):
        return str(v)