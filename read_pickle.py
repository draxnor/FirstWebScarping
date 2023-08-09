import pickle
from pprint import pprint


if __name__ == '__main__':
    with open('product_list.pkl', 'rb') as fp:
        product_list = pickle.load(fp)

    pprint(product_list)
    # for product in product_list:
    #
    #     print(f'Product: {product["name"]}', f'Price: {product["price"]}', sep='\n')
