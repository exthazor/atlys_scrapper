from pydantic import BaseModel, HttpUrl, Field, validator

class Product(BaseModel):
    title: str = Field(..., alias='product_title')
    price: float = Field(..., alias='product_price')
    image_url: str = Field(..., alias='path_to_image')

    @validator('price', pre=True)
    def parse_price(cls, value):
        if isinstance(value, str):
            value = value.replace('₹', '').replace(',', '').strip()
        return float(value)

    class Config:
        allow_population_by_field_name = True
