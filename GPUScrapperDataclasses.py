from dataclasses import dataclass
import datetime


@dataclass()
class Shop:
    shop_id: int
    shop_name: str
    shop_url: str


@dataclass()
class GraphicCard:
    card_id: int
    card_name: str
    card_ean: str
    card_producent_code: str
    card_producent: str
    card_chipset: str
    chipset_producent: str
    card_memory_in_gbs: int
    card_memory_type: str


@dataclass()
class Price:
    shop_id: int
    card_id: int
    price: float
    data_collection_datetime: datetime.datetime
