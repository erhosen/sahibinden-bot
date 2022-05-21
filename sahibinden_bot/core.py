from typing import List

from pydantic import BaseModel


class SahibindenMeta(BaseModel):
    published_ids: List[int]


class Product(BaseModel):
    id: int
    link: str
    image: str
    title: str
    price: str
    location: str

    def to_message(self) -> str:
        return (
            f'Advert: <a href="{self.link}">{self.title}</a>\n'
            f"Price: <b>{self.price}</b>\n"
            f'Location: <a href="https://www.google.com/maps/search/?api=1&query={self.location}">{self.location}</a>'
        )
