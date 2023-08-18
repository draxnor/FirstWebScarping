from dataclasses import dataclass
import datetime


@dataclass()
class Shop:
    shop_name: str
    shop_base_url: str
    gpu_category_url: str

@dataclass()
class GraphicCard:
    card_name: str
    card_ean: str
    card_producent_code: str
    card_producent: str
    card_chipset: str
    chipset_producent: str
    card_memory_in_gbs: float
    card_memory_type: str
    card_price: float
    data_collection_datetime: datetime.datetime
