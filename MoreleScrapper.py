import sys
import requests
from bs4 import BeautifulSoup
import logging
from GPUScrapperDataclasses import Shop, GraphicCardOffer
from datetime import datetime
from math import isnan
import re


class MoreleScraper:
    shop = Shop(shop_name='morele',
                shop_base_url='https://www.morele.net',
                category_url='/kategoria/karty-graficzne-12/')

    def scrap(self) -> list:
        offers = []
        product_urls = self.scrap_for_product_urls()
        for product_relative_url in product_urls:
            offer_data = self._scrap_product_page(product_relative_url)
            offers.append(offer_data)
        return offers

    def scrap_for_product_urls(self) -> list[str]:
        current_category_page_relative_url = self.shop.category_url
        all_product_urls = []

        is_last_page = False
        counter = 0 #todo
        while not is_last_page:
            current_category_page_url = ''.join((self.shop.shop_base_url, current_category_page_relative_url))
            logging.info(f'Scraping category page: {current_category_page_url}')
            products_urls, next_category_page_relative_url = self._scrap_category_page(current_category_page_url)
            current_category_page_relative_url = next_category_page_relative_url
            all_product_urls += products_urls
            counter += 1
            if current_category_page_relative_url is None or counter > 0:
                is_last_page = True
                logging.info(f'Finished scrapping category pages for product urls '
                             f'from {self.shop.shop_name} online shop!')
        return all_product_urls

    def _scrap_category_page(self, category_url):
        html_content = requests.get(category_url)
        soup_doc = BeautifulSoup(html_content.text, 'html.parser')
        product_urls = self._get_product_urls_from_category_page(soup_doc)
        next_category_page_relative_url = self._get_next_page_url(soup_doc)
        return product_urls, next_category_page_relative_url

    def _get_next_page_url(self, soup: BeautifulSoup):
        if not (next_button_section := soup.select_one('li.pagination-lg.next')):
            return None
        if not (link := next_button_section.select_one('a.pagination-btn')):
            return None
        return link.get('href', None)

    def _get_product_urls_from_category_page(self, soup: BeautifulSoup) -> list[str]:
        if not (product_list_section := soup.select_one('div.cat-list-products')):
            return []
        if not (links_soup := product_list_section.select('a.productLink')):
            return []
        products_urls = list(set(link.get('href') for link in links_soup))
        return products_urls

    def _scrap_product_page(self, product_relative_url):
        product_url = self.shop.shop_base_url + product_relative_url
        request_result = requests.get(product_url)
        page_content = request_result.text
        page_soup = BeautifulSoup(page_content, 'html.parser')
        gpu_offer_dict = self._get_product_specification(page_soup)
        gpu_offer_dict['url'] = product_url
        gpu_offer = GraphicCardOffer(**gpu_offer_dict)
        return gpu_offer

    def _get_specification_detail_from_specification_table(self,
                                                           specification_table_soup,
                                                           spec_detail_translated_name: str
                                                           ) -> str | None:
        spec_name_section = specification_table_soup.find('span', string=spec_detail_translated_name)
        if not spec_name_section:
            logging.info(f"Could not find {spec_detail_translated_name} in specification table.")
            return None

        if not ('specification__name' in spec_name_section.get('class', '')):
            spec_name_section = spec_name_section.find_parent('span', class_='specification__name')
        if not spec_name_section:
            logging.info(f"Could not find 'specification__name' section for {spec_detail_translated_name}.")
            return None

        specification_value_soup = spec_name_section.find_next_sibling('span', class_="specification__value")
        if not specification_value_soup:
            logging.info(f"Could not find 'specification__value' for '{spec_detail_translated_name}'. ")
            return None
        specification_value_text_element = specification_value_soup.find(string=lambda s: bool(s.strip()))
        if not specification_value_text_element:
            logging.info(f"Could not find any string in 'specification__value' for '{spec_detail_translated_name}'. ")
            return None
        specification_value_as_string = str(specification_value_text_element).strip()
        return specification_value_as_string

    def _get_product_price(self, product_page_soup):
        price_soup = product_page_soup.find('div', id='product_price_brutto', class_='product-price')
        product_price_str = price_soup.get('data-price', None) if price_soup else None
        product_price = float(product_price_str) if product_price_str is not None else None
        return product_price

    def _get_product_name(self, product_page_soup):
        if not (prod_name_section := product_page_soup.select_one('div.prod-name-wr')):
            return None
        if not (product_name_soup := prod_name_section.select_one('h1.prod-name')):
            return None
        product_name = str(product_name_soup.get('data-default'))
        return product_name

    def _get_product_specification(self, product_page_soup):
        specification_table_names_translation = {
            'card_ean': 'EAN',
            'card_producent_code': 'Kod producenta',
            'card_producent': 'Producent',
            'card_chipset': 'Rodzaj chipsetu',
            'chipset_producent': 'Producent chipsetu',
            'card_memory_in_gbs': 'Ilość pamięci RAM',
            'card_memory_type': 'Rodzaj pamięci RAM'
        }

        offer_details_dict = {}
        for spec_name, spec_name_translation in specification_table_names_translation.items():
            offer_details_dict[spec_name] = self._get_specification_detail_from_specification_table(product_page_soup,
                                                                                                    spec_name_translation)
        offer_details_dict['card_name'] = self._get_product_name(product_page_soup)
        offer_details_dict['card_price'] = self._get_product_price(product_page_soup)
        offer_details_dict['data_collection_datetime'] = datetime.now()

        clean_offer_details = self._clean_offer_data(offer_details_dict)

        return clean_offer_details

    def _clean_offer_data(self, gpu_offer_dict):
        if gpu_offer_dict.get('card_memory_in_gbs') is not None:
            card_memory_string = gpu_offer_dict['card_memory_in_gbs']
            decimals_from_field = re.findall(r'\d+', card_memory_string)
            memory_in_gbs = int(decimals_from_field[0]) if decimals_from_field else None
            if re.search('mb', card_memory_string, re.IGNORECASE):
                gpu_offer_dict['card_memory_in_gbs'] = round(memory_in_gbs / 1000, 3)
            else:
                gpu_offer_dict['card_memory_in_gbs'] = memory_in_gbs
        card_name = gpu_offer_dict.get('card_name').removeprefix('Karta graficzna').strip()
        gpu_offer_dict['card_name'] = card_name

        return gpu_offer_dict
