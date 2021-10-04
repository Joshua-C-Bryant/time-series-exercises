import pandas as pd 
import requests
import os

base_url = 'https://python.zgulde.net'


def get_items_data():
    response = requests.get(base_url + '/api/v1/items')
    data = response.json()
    items_df = pd.DataFrame(data['payload']['items'])
    response = requests.get(base_url + data['payload']['next_page'])
    data = response.json()
    df = pd.concat([items_df, pd.DataFrame(data['payload']['items'])]).reset_index()
    response = requests.get(base_url + data['payload']['next_page'])
    data = response.json()
    items_df = pd.concat([df, pd.DataFrame(data['payload']['items'])]).reset_index()
    return items_df

def get_stores_data():
    response = requests.get(base_url + '/api/v1/stores')
    data =  response.json()
    stores_df = pd.DataFrame(data['payload']['stores'])
    return stores_df

def get_sales_data():
    response = requests.get(base_url + '/api/v1/sales')
    filename = 'sales.csv'
    if os.path.isfile(filename):
        sales = pd.read_csv(filename, index_col=[0])
    else:
        if response.ok:
            extracted_data = list()
            payload = response.json()['payload']
            max_page = payload['max_page']
            for n in range(max_page):
                extracted_data.extend(payload['sales'])
                try:
                    new_url = url[:25] + payload['next_page']
                    print(new_url)
                    response = requests.get(new_url)
                    payload = response.json()['payload']
                except:
                    pass
                
            sales = pd.DataFrame(extracted_data)
            sales.to_csv(filename)

        else:
            print(response.status_codeus_code)
    return sales

def get_store_data():
    items_df = get_items_data()
    stores_df = get_stores_data()
    sales_df = get_sales_data()
    sales_plus_stores = pd.merge(sales_df, stores_df, how='left', left_on='store', right_on='store_id')
    df = pd.merge(sales_plus_stores, items_df, how='left', left_on='item', right_on='item_id')
    return df