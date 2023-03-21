import pandas as pd
from sqlalchemy import create_engine, exc
from selenium import webdriver
from selenium.webdriver.common.by import By

def get_tickers (page = None) :
    #Search for existing tickers in the finance and scrap them

    #Not used yet
    if(page == None) :
        url = "https://marketstack.com/search"
    else :
        url = "https://marketstack.com/search"
    
    #Start a selenium session
    options = webdriver.FirefoxOptions()
    options.add_argument("--private")
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.get(url)

    #Scrap the tickers
    datas = driver.find_elements(By.XPATH, "//tbody//tr")

    #Add all the tickers to a dataframe
    list_results = list()
    for d in datas :
        list_results.append(d.text.split(" ")[0].replace(".","-"))
    df_tickers = pd.DataFrame(list_results, columns=["Symbols"])

    #Store the tickers in the database
    engine = create_engine('sqlite:///datas_stock/stocks.db')
    df_tickers.to_sql("stocks", engine, if_exists='replace', index=False)
    
    #Close the session
    driver.close()


    


