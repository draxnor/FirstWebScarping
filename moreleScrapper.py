import requests
from bs4 import BeautifulSoup
import pickle
from GPUScrapperDataclasses import Shop, GraphicCard, Price
from pprint import pprint


def get_html_content(url):
    content = requests.get(url)
    return content.text


def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup


def get_next_page_url(soup):
    if not (next_button_section := soup.select_one('li.pagination-lg.next')):
        return None
    if not (link := next_button_section.select_one('a.pagination-btn')):
        return None
    return link.get('href', None)


def get_links_to_products(soup) -> list[str]:
    if not (product_list_section := soup.select_one('div.cat-list-products')):
        return []
    if not (links_soup := product_list_section.select('a.productLink')):
        return []
    products_urls = list(set(link.get('href') for link in links_soup))
    return products_urls


if __name__ == '__main__':
    base_url = 'https://www.morele.net'
    relative_url = '/kategoria/karty-graficzne-12/'
    products_urls = []

    is_last_page = False
    while not is_last_page:
        url = ''.join((base_url, relative_url))
        print(url)
        html_content = get_html_content(url)
        soup_doc = parse_html(html_content)
        products_urls.extend(get_links_to_products(soup_doc))
        relative_url = get_next_page_url(soup_doc)
        if relative_url is None:
            is_last_page = True
            print('Finished!')

    # with open('morele_products_links.txt', 'w') as f:
    #     f.write('\n'.join(products_urls))
    # with open('morele_products_links.pkl', 'wb') as f:
    #     pickle.dump(products_urls, f)