from typing import Protocol


class Scrapper(Protocol):
    def scrap(self):
        ...
