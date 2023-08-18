import requests
from bs4 import BeautifulSoup
import logging
import pickle
from GPUScrapperDataclasses import Shop, GraphicCard
from pprint import pprint


class MoreleScraper:
    shop = Shop(shop_name='morele',
                shop_base_url='https://www.morele.net',
                gpu_category_url='/kategoria/karty-graficzne-12/')

    def scrap(self):
        pass

    def scrap_for_product_urls(self):
        #TODO handling request connection error
        current_category_page_relative_url = self.shop.gpu_category_url
        all_product_urls = []

        is_last_page = False
        while not is_last_page:
            current_category_page_url = ''.join((self.shop.shop_base_url, current_category_page_relative_url))
            logging.info(f'Scraping category page: {current_category_page_url}')
            products_urls, next_category_page_relative_url = self.scrap_category_page(current_category_page_url)
            all_product_urls += products_urls
            current_category_page_relative_url = next_category_page_relative_url
            if current_category_page_relative_url is None:
                is_last_page = True
                logging.info(f'Finished scrapping product urls from {self.shop.shop_name} online shop!')
        return all_product_urls

    def scrap_product_page(self, product_url):
        pass

    def scrap_category_page(self, category_url):
        html_content = get_html_content(category_url)
        soup_doc = parse_html(html_content)
        product_urls = get_links_to_products(soup_doc)
        next_category_page_relative_url = self.get_next_page_url(soup_doc)
        return product_urls, next_category_page_relative_url

    def feed_database(self):
        pass

    def dump_to_file(self, file):
        pass

    def get_last_update_datetime(self):
        pass
    def get_next_page_url(self, soup):
        if not (next_button_section := soup.select_one('li.pagination-lg.next')):
            return None
        if not (link := next_button_section.select_one('a.pagination-btn')):
            return None
        return link.get('href', None)

def get_html_content(url):
    content = requests.get(url)
    return content.text


def parse_html(html_content) -> BeautifulSoup:
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup





def get_links_to_products(soup) -> list[str]:
    if not (product_list_section := soup.select_one('div.cat-list-products')):
        return []
    if not (links_soup := product_list_section.select('a.productLink')):
        return []
    products_urls = list(set(link.get('href') for link in links_soup))
    return products_urls


if __name__ == '__main__':
    pass

    # with open('morele_products_links.txt', 'w') as f:
    #     f.write('\n'.join(products_urls))
    # with open('morele_products_links.pkl', 'wb') as f:
    #     pickle.dump(products_urls, f)