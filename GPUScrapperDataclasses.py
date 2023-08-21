from dataclasses import dataclass
import datetime


@dataclass()
class Shop:
    shop_name: str
    shop_base_url: str
    category_url: str

@dataclass()
class GraphicCardOffer:
    card_name: str
    card_ean: str
    card_producent_code: str
    card_producent: str
    card_chipset: str
    chipset_producent: str
    card_memory_in_gbs: float
    card_memory_type: str
    card_price: float
    url: str
    data_collection_datetime: datetime.datetime
