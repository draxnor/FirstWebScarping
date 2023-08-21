import sys

from MoreleScrapper import MoreleScraper
from pprint import pprint
from MySQLPipeline import MySqlPipeline
import logging

#TODO
#updating Null column values for existing records in GraphicCard table
#adding new shops

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    mysql_manager = MySqlPipeline()
    scrapper = MoreleScraper()
    gpu_offers = scrapper.scrap()
    mysql_manager.save_offers_to_database(gpu_offers, scrapper.shop)
    pprint(gpu_offers)


