from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.common.exceptions as ex
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import pandas as pd
from sqlalchemy import create_engine, exc

def stock_to_df(stock, start_scrap = None, end_scrap = None) : 
    #Scrap a stock page from the Yahoo finance website.

    engine = create_engine('sqlite:///datas_stock/stocks.db')
    list_results = list()

    #Check if a time period is given and change the url according to that
    if (start_scrap == None and end_scrap == None):
        url = f"https://finance.yahoo.com/quote/{stock}/history?p={stock}"
    else:
        start_scrap = int(time.mktime(time.strptime(f'{start_scrap} 02:00:00', '%Y-%m-%d %H:%M:%S')))
        end_scrap = int(time.mktime(time.strptime(f'{end_scrap} 02:00:00', '%Y-%m-%d %H:%M:%S')))
        url = f"https://finance.yahoo.com/quote/{stock}/history?period1={start_scrap}&period2={end_scrap}&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true"
    
    #Start a selenium session
    options = webdriver.FirefoxOptions()
    options.add_argument("--private")
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    driver.get(url)

    #Click on some buttons to delete pop up
    try :
        scroll_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@id='scroll-down-btn']"))
        )
        scroll_button.click()

        cookies_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='btn secondary accept-all ']"))
        )
        cookies_button.click()

        subscribe_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='Pos(a) T(20px) End(20px) P(4px) Bd(0) Bgc(t) M(0)']"))
        )
        subscribe_button.click()
    except(ex.TimeoutException) :
        return

    #Scrap all the needed datas
    name_stock = driver.find_element(By.XPATH, "//h1[@class='D(ib) Fz(18px)']").text
    datas = driver.find_elements(By.XPATH, "//tr[@class='BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)']")

    #Filter the datas to keep only the "Adj Close" and the date
    for d in datas :
        data = d.text
        regex_pattern = r"([a-zA-Z]{3})\s+(\d{1,2}),\s+(\d{4})"

        match = re.search(regex_pattern, data)
        if match:
            month_abbr = match.group(1)
            day = match.group(2)
            year = match.group(3)

            month_dict = {
                'Jan': '01',
                'Feb': '02',
                'Mar': '03',
                'Apr': '04',
                'May': '05',
                'Jun': '06',
                'Jul': '07',
                'Aug': '08',
                'Sep': '09',
                'Oct': '10',
                'Nov': '11',
                'Dec': '12'
            }
            month_num = month_dict.get(month_abbr, '00')

            new_date_string = f"{year}-{month_num}-{day.zfill(2)}"

            values = data.split()
            penultimate_value = values[-2]

            result = (new_date_string, penultimate_value)

            list_results.append(result)

    #Close the session and create a dataframe with the result
    driver.close()
    df_stock = pd.DataFrame(list_results, columns=["Date", "Adj Close"])

    #Add the result to the "stock" database and return the result dataframe
    try :
        df_existing = pd.read_sql(name_stock, engine)
        df_merged = pd.merge(df_existing, df_stock, on=['Date', name_stock], how='outer')
        df_merged.to_sql(name_stock, engine, if_exists='replace', index=False)
        return df_merged
    except (exc.OperationalError) :
        df_stock.to_sql(name_stock, engine, index=False)
        return df_stock

