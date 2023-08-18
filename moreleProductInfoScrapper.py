import sys

from bs4 import BeautifulSoup
from MoreleScrapper import get_html_content, parse_html
import pickle
from pprint import pprint
from datetime import datetime


def get_specification_detail_from_table(specification_table_soup, spec_detail_translated_name: str) -> str | None:
    spec_name_section = specification_table_soup.find('span', string=spec_detail_translated_name)
    if not spec_name_section:
        print(f"Could not find {spec_detail_translated_name} in specification table.", file=sys.stderr)
        return None

    if not ('specification__name' in spec_name_section.get('class', '')):
        spec_name_section = spec_name_section.find_parent('span', class_='specification__name')
    if not spec_name_section:
        print(f"Could not find 'specification__name' section for {spec_detail_translated_name}.")
        return None

    specification_value_soup = spec_name_section.find_next_sibling('span', class_="specification__value")
    if not specification_value_soup:
        print(f"Could not find 'specification__value' for '{spec_detail_translated_name}'. ", file=sys.stderr)
        return None
    specification_value_text_element = specification_value_soup.find(string=lambda s: bool(s.strip()))
    if not specification_value_text_element:
        print(f"Could not find any string in 'specification__value' for '{spec_detail_translated_name}'. ",
              file=sys.stderr)
        return None
    specification_value_as_string = str(specification_value_text_element).strip()
    return specification_value_as_string


def get_product_price(page_soup):
    price_soup = page_soup.find('div', id='product_price_brutto', class_='product-price')
    product_price_str = None
    if price_soup:
        product_price_str = price_soup.get('data-price', None)
    product_price = float(product_price_str) if product_price_str is not None else None
    return product_price


def get_product_name(page_soup):
    if not (prod_name_section := page_soup.select_one('div.prod-name-wr')):
        return None
    if not (product_name_soup := prod_name_section.select_one('h1.prod-name')):
        return None
    product_name = str(product_name_soup.get('data-default'))
    return product_name


def get_product_specification(product_page_soup):
    specification_table_names_translation = {
        'card_ean': 'EAN',
        'card_producent_code': 'Kod producenta',
        'card_producent': 'Producent',
        'card_chipset': 'Rodzaj chipsetu',
        'chipset_producent': 'Producent chipsetu',
        'card_memory_in_gbs': 'Ilość pamięci RAM',
        'card_memory_type': 'Rodzaj pamięci RAM'
    }

    specification = {}
    for spec_name, spec_name_translation in specification_table_names_translation.items():
        specification[spec_name] = get_specification_detail_from_table(product_page_soup, spec_name_translation)
    specification['card_name'] = get_product_name(product_page_soup)
    specification['card_price'] = get_product_price(product_page_soup)
    specification['data_collection_datetime'] = datetime.now()

    return specification


if __name__ == '__main__':
    with open('morele_products_links.pkl', 'rb') as f:
        product_urls = pickle.load(f)

    product_info = []
    base_url = 'https://www.morele.net'
    try:
        for product_relative_url in product_urls:
            url = base_url + product_relative_url
            print(url)
            page_content = get_html_content(url)
            page_soup = parse_html(page_content)
            product_specification = get_product_specification(page_soup)
            product_info.append(product_specification)
            pprint(product_specification)
            print('\n'*3)
    finally:
        with open('morele_products_info.pkl', 'wb') as f:
            pickle.dump(product_info, f)

