from sqlalchemy import create_engine, MetaData
import pandas as pd


user = 'yarik'
password = 'admin'
host = '127.0.0.1'
port = '3306'
database = 'kijijidatadb'

meta = MetaData()

engine = create_engine(f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}')
meta.create_all(engine)

apartments = meta.tables['Apartments']
conn = engine.connect()
apartments_output_query = apartments.select()
apSet = conn.execute(apartments_output_query)
columns = apartments.c

df = pd.DataFrame(apSet, columns=columns)
print(df)
