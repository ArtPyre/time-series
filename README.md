# time-series

Collect financial informations and store them in a database to be use later in a portofiolo

## datas_stock

A folder that contains all the scrapper needed and the database

### tickers_scrapper

Collect tickers from the https://marketstack.com website for scrapping. Then store them in the database "stocks" in the table "stocks"

### stock_scrapper

Use the tickers scrapped previously the get finance information from them on the https://finance.yahoo.com/ and scrap them for the use of a portfolio. Then store each tickers in a table in the database, if the table already exist, append all the datas.

### getting_datas

Create the database.

## dags

In progress

## Authors

Contributors names and contact info

* Pyre Arthur