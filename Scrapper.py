from typing import Protocol


class Scrapper(Protocol):
    def scrap(self):
        ...

    def feed_database(self):
        ...

    def dump_to_file(self, file):
        ...

    def get_last_update_datetime(self):
        ...
