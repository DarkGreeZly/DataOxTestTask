from sqlalchemy import create_engine, MetaData, Table, Integer, Column, String
import pandas as pd
import openpyxl

user = 'yarik'
password = 'admin'
host = '127.0.0.1'
port = '3306'
database = 'kijijidatadb'

meta = MetaData()

apartments = Table('Apartments', meta,
                   Column('id', Integer, primary_key=True),
                   Column('title', String(250), nullable=False),
                   Column('location', String(250), nullable=False),
                   Column('date_of_published', String(250), nullable=False),
                   Column('price', String(250), nullable=False),
                   Column('currency', String(250), nullable=False),
                   Column('image_url', String(250), nullable=False),
                   Column('bedroom', String(250), nullable=False),
                   Column('description', String(2500), nullable=False))

engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}')
meta.create_all(engine)

conn = engine.connect()

def insert_elements(titles, locations, dates, prices, currencies, images, bedrooms, descriptions):
    for i in range(0, len(titles) + 1):
        apartments_query = apartments.insert().values(title=titles[i], location=locations[i],
                                                  date_of_published=dates[i], price=prices[i], currency=currencies[i],
                                                  image_url=images[i], bedroom=bedrooms[i], description=descriptions[i])
        conn.execute(apartments_query)

def select_elements():
    apartments_output_query = apartments.select()
    res = conn.execute(apartments_output_query)
    for row in res:
        print(row)

def delete_elements():
    apartments_output_query = apartments.delete()
    res = conn.execute(apartments_output_query)

def dump_to_xlsx():
    apartments_output_query = apartments.select()
    res = conn.execute(apartments_output_query)
    df = pd.DataFrame(res)
    df.to_excel('./kijijidata.xlsx')