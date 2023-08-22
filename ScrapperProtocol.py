from typing import Protocol
from GPUScrapperDataclasses import Shop


class ScrapperProtocol(Protocol):
    shop: Shop
    
    def scrap(self):
        ...


