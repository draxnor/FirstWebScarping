import logging
import mysql.connector
from GPUScrapperDataclasses import GraphicCardOffer, Shop
from dataclasses import asdict
import datetime


class MySqlPipeline:
    def __init__(self):
        self.connection = mysql.connector.connect(host='localhost',
                                                  database='Graphic_Card_Prices',
                                                  user='gpu_scrapper',
                                                  password='kochamolge123.')
        if self.connection.is_connected():
            logging.info('MySQL database connection successfully established.')

        self.cursor = self.connection.cursor()
        self._database_tables_init()

    def _database_tables_init(self):
        create_shop_query = """
                        CREATE TABLE IF NOT EXISTS Shop (
                        Shop_ID INT AUTO_INCREMENT,
                        Shop_Name VARCHAR(255),
                        Shop_URL VARCHAR(255),
                        Last_Update_Datetime DATETIME,
                        PRIMARY KEY (Shop_ID)
                        );
                        """
        create_graphiccard_query = """
                                    CREATE TABLE IF NOT EXISTS GraphicCard (
                                        Card_ID INT AUTO_INCREMENT,
                                        Card_Name VARCHAR(255),
                                        Card_EAN VARCHAR(13) UNIQUE,
                                        Card_Producent_Code VARCHAR(100),
                                        Card_Producent VARCHAR(50),
                                        Card_Chipset VARCHAR(100),
                                        Chipset_Producent VARCHAR(50),
                                        Card_Memory_in_GBs DECIMAL(10,3),
                                        Card_Memory_Type VARCHAR(50),
                                        PRIMARY KEY (Card_ID)
                                    );
                                    """
        create_offer_query = """
                            CREATE TABLE IF NOT EXISTS Offer (
                                Offer_ID INT AUTO_INCREMENT,
                                Offer_URL VARCHAR(255),
                                Shop_ID INT,
                                Card_ID INT,
                                Card_Price DECIMAL(10,2),
                                Data_Collection_Datetime DATETIME,
                                PRIMARY KEY (Offer_ID),
                                FOREIGN KEY (Shop_ID) REFERENCES Shop(Shop_ID),
                                FOREIGN KEY (Card_ID) REFERENCES GraphicCard(Card_ID)
                            );
                            """
        self.cursor.execute(create_shop_query)
        self.cursor.execute(create_graphiccard_query)
        self.cursor.execute(create_offer_query)
        self.connection.commit()

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
            logging.info('MySQL database connection closed.')

    def __del__(self):
        self.close_connection()

    def get_shop_id_by_name(self, shop_name):
        shop_id_query = """
                SELECT
                    shop_id
                FROM
                    shop
                WHERE
                    shop_name = %s
                """
        # cursor = self.connection.cursor()
        self.cursor.execute(shop_id_query, (shop_name,))
        query_result = self.cursor.fetchall()
        # cursor.close()
        if not query_result:
            return None
        if len(query_result) > 1:
            logging.warning('More than 1 shop with same name in database.')
        shop_id = query_result.pop()[0]
        return shop_id

    def get_graphic_card_id_from_db(self, gpu_offer: GraphicCardOffer):
        card_id_query = """
                SELECT
                    card_id
                FROM
                    GraphicCard
                WHERE
                    card_ean = %(card_ean)s
                    OR card_producent_code = %(card_producent_code)s
                    OR (card_ean IS NULL 
                        AND card_producent_code IS NULL
                        AND card_name = %(card_name)s)
                """

        logging.info(f"Trying to get ID of card with EAN: '{gpu_offer.card_ean}' "
                     f"and producent code: '{gpu_offer.card_producent_code}'")
        # cursor = self.connection.cursor()
        self.cursor.execute(card_id_query, asdict(gpu_offer))
        card_id_query_result = self.cursor.fetchall()
        # cursor.close()
        if not card_id_query_result:
            return None
        if len(card_id_query_result) > 1:
            logging.warning('More than 1 shop with same name in database.')
        card_id_queried = card_id_query_result.pop()[0]
        return card_id_queried

    def insert_gpu_offer_to_db(self, gpu_offer: GraphicCardOffer) -> int:
        gpu_data_insertion_query = """
                    INSERT INTO
                        GraphicCard (
                            card_name,
                            card_ean,
                            card_producent_code,
                            card_producent,
                            card_chipset,
                            chipset_producent,
                            card_memory_in_GBs,
                            card_memory_type
                            )
                    VALUES (
                        %(card_name)s,
                        %(card_ean)s,
                        %(card_producent_code)s,
                        %(card_producent)s,
                        %(card_chipset)s,
                        %(chipset_producent)s,
                        %(card_memory_in_gbs)s,
                        %(card_memory_type)s
                        )
                    """
        logging.info(f"Inserting: {asdict(gpu_offer)}")

        # cursor = self.connection.cursor()
        self.cursor.execute(gpu_data_insertion_query, asdict(gpu_offer))
        card_id = self.cursor.lastrowid
        self.connection.commit()
        # cursor.close()

        return card_id

    def insert_price_to_db(self, shop_id: int, card_id: int, gpu_offer_details: GraphicCardOffer):
        add_price_query = """
                            INSERT INTO
                                Offer(
                                    Shop_ID,
                                    Card_ID,
                                    Card_Price,
                                    Offer_URL,
                                    Data_collection_datetime
                                    )
                            VALUES (
                                %(shop_id)s,
                                %(card_id)s,
                                %(card_price)s,
                                %(offer_url)s,
                                %(data_collection_datetime)s
                                )
                           """
        # cursor = self.connection.cursor()
        self.cursor.execute(add_price_query, {'shop_id': shop_id,
                                              'card_id': card_id,
                                              'card_price': gpu_offer_details.card_price,
                                              'offer_url': gpu_offer_details.url,
                                              'data_collection_datetime': gpu_offer_details.data_collection_datetime
                                              })
        offer_id = self.cursor.lastrowid
        self.connection.commit()
        # cursor.close()
        return offer_id

    def insert_shop_to_db(self, shop: Shop):
        insert_shop_query = """
                            INSERT INTO
                                Shop (
                                    Shop_Name,
                                    Shop_URL
                                    )
                            VALUES (
                            %(shop_name)s
                            %(shop_base_url)s
                            )
                            """
        # cursor = self.connection.cursor()
        self.cursor.execute(insert_shop_query, asdict(shop))
        shop_id = self.cursor.lastrowid
        self.connection.commit()
        # cursor.close()
        return shop_id

    def update_shop_last_update_datetime(self, shop_name, last_update_datetime: datetime.datetime):
        update_last_update_datetime_query = """
                                            UPDATE
                                                Shop
                                            SET 
                                                Last_Update_Datetime = %(last_update_datetime)s
                                            WHERE
                                                shop_name = %(shop_name)s
                                            """
        # cursor = self.connection.cursor()
        self.cursor.execute(update_last_update_datetime_query, {'shop_name': shop_name,
                                                                'last_update_datetime': last_update_datetime})
        self.connection.commit()
        # cursor.close()

    def save_offers_to_database(self, offers: list[GraphicCardOffer], shop: Shop):
        shop_id = self.get_shop_id_by_name(shop.shop_name)
        for offer in offers:
            self._save_offer_to_database(offer, shop_id)

    def _save_offer_to_database(self, offer: GraphicCardOffer, shop_id: int):
        card_id = self.get_graphic_card_id_from_db(offer)
        if card_id is None:
            card_id = self.insert_gpu_offer_to_db(offer)
        offer_id = self.insert_price_to_db(shop_id, card_id, offer)
        return shop_id, card_id, offer_id




