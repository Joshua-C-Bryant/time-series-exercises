import numpy as np
import pandas as pd
from datetime import timedelta, datetime

# Prep Store Data

def prep_store_data(df):
    # drop unecessary columns
    df = df.drop(columns = ['item','level_0','index','store'])
    # convert sales date to datetime
    df.sale_date = pd.to_datetime(df.sale_date).dt.date
    df['sale_date']= pd.to_datetime(df['sale_date'])
    # create month column
    df['month'] = df.sale_date.dt.month
    # create day of the week column
    df['day_of_week'] = df.sale_date.dt.day_of_week
    # rest index to be in chronological order
    df = df.set_index('sale_date').sort_index()
    # create sales_total column, which is the quantity * price
    df['sales_total'] = df.sale_amount * df.item_price
    return df

# Prep OPSD Data

def pre_opsd_data():
    # acquire 
    df = pd.read_csv('https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv')
    # convert column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    # create month and year columns
    df['month'] = df.Date.dt.month
    df['year'] = df.Date.dt.year
    # fill nulls
    df.fillna(0,inplace=True)
    # reset index
    df = df.set_index(df.Date)
    return df