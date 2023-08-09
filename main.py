from pprint import pprint
import requests
from bs4 import BeautifulSoup
import pickle


def parse_graphic_card_name(item_section):
    item_description = item_section['data-product-name']
    desc_without_prefix = item_description.lstrip('Karta graficzna ')
    bracket_opening_idx = desc_without_prefix.find("(")
    bracket_enclosing_idx = desc_without_prefix.find(")")
    full_model_name = desc_without_prefix[:bracket_opening_idx].rstrip()
    model_id = desc_without_prefix[bracket_opening_idx+1: bracket_enclosing_idx].strip()
    return full_model_name, model_id


def get_chipset_type(item_section):
    features = item_section.find_all('div', class_='cat-product-feature')
    chipset_type = 'Not found'
    for feature in features:
        if 'Rodzaj chipsetu:' in feature.text:
            chipset_type = feature.find('b').text
            break
    return chipset_type

def get_card_product_list(bs_single_page):
    graphic_card_sections = bs_single_page.find_all(['div'], class_='card')

    product_list = []
    for item_section in graphic_card_sections:
        if 'data-product-name' not in item_section.attrs:
            continue

        chipset_type = get_chipset_type(item_section)
        model_name, model_id = parse_graphic_card_name(item_section)
        brand = item_section.get('data-product-brand')
        price = item_section.get('data-product-price')
        product_info = {
            'name': model_name,
            'id': model_id,
            'brand': brand,
            'price': price,
            'chipset': chipset_type
        }
        product_list.append(product_info)
    return product_list


def main():
    url_base = 'https://www.morele.net/kategoria/karty-graficzne-12/,,,,,,,,0,,,,/'
    full_product_list = []
    for page_index in range(1, 25):
        url = url_base + str(page_index) + '/'
        result = requests.get(url)
        doc = BeautifulSoup(result.text, 'html.parser')
        card_list = get_card_product_list(doc)
        full_product_list.extend(card_list)
    with open('product_list.pkl', 'wb') as fp:
        pickle.dump(full_product_list, fp)
        print('File saved successfully.')
    # pprint(full_product_list)


if __name__ == '__main__':
    main()

