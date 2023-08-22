from MoreleScrapper import MoreleScraper
from MySQLPipeline import MySqlPipeline
from ScrapperProtocol import ScrapperProtocol
import logging

#TODO
#updating Null column values for existing records in GraphicCard table
#adding new shops


def scrap_and_save_to_db(scrapper: ScrapperProtocol, db_manager: MySqlPipeline):
    gpu_offers = scrapper.scrap()
    db_manager.save_offers_to_database(gpu_offers, scrapper.shop)
    logging.info(f'Scrapper for shop: {scrapper.shop.shop_name} has finished its task. '
                 f'{len(gpu_offers)} offers added to database')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    mysql_manager = MySqlPipeline()
    scrapper = MoreleScraper()
    scrap_and_save_to_db(scrapper, mysql_manager)


