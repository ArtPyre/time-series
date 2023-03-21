from sqlalchemy import create_engine, exc
import pandas as pd
import time
import stock_scrapper, tickers_scrapper

start_time = "2023-01-01"
end_time = "2023-03-01"

engine = create_engine('sqlite:///datas_stock/stocks.db')

#Scrap some tickers if none is found on the DB
try:
    df_tickers = pd.read_sql('stocks', engine)
except (exc.OperationalError) :
    print("no DB found")  
    tickers_scrapper.get_tickers()
    df_tickers = pd.read_sql('stocks', engine)
    
#Scrap the tickers_list's datas from a certain time
tickers = df_tickers.values
for t in tickers :
    scrap_time = time.perf_counter()
    stock_scrapper.stock_to_df(t[0], start_time, end_time)
    print(f"stock {t[0]} took {time.perf_counter() - scrap_time} seconds to process")
