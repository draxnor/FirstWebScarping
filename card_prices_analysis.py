import pickle
from pprint import pprint
import pandas as pd

if __name__ == '__main__':
    with open('product_list.pkl', 'rb') as fp:
        product_list = pickle.load(fp)

    product_list.sort(key=lambda el: el['price'])
    products = pd.DataFrame(product_list)

    # Group by chipsets and show minimum and median of a price
    rxs_and_rtxs = products[products['chipset'].str.contains('Radeon RX|GeForce RTX')]
    result = rxs_and_rtxs.groupby(by=['chipset']).agg({'price': ['min', 'median']})
    pprint(result)

    # # List all chipsets available
    # print('\n'.join(products['chipset'].unique().tolist()))

    # # List all products with chosen chipset
    # pprint(products[['name', 'price']].loc(products['chipset'] == 'GeForce RTX 3060'))



