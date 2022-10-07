import pandas      as pd
import yfinance    as yf
import fundamentus as fd
import csv   
import os
import datetime


# Variables dynamics
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)


# Open archive in cod actions
with open('./source/ListStocks.csv', newline='') as file:
     file_reader = csv.reader(file)
     my_list = list(file_reader)
     
     for stock in my_list:
         dados = yf.download(stock[0]  + '.SA', start=yesterday, end=today, actions=False)
         cotacao = dados["Adj Close"]
         
         # Gravando os dados de preço
         with open('./source/Stocks.csv', 'a', encoding="utf-8") as f:
              result = stock[0] + ';' + str(cotacao[0])+ '\n'
              print(stock[0].upper() + ' sendo gravado!')
              f.write(result)

# DataFrame of indicators
stock_indicators = fd.get_resultado()

# Importing csv data from yesterday's quote
stock_csv = pd.read_csv('./source/Stocks.csv', sep=";")
stock_value = pd.DataFrame(stock_csv)

# Merged Dataframes
stock_value.columns = ['papel','cotacao_ontem']
stock_dataframe = pd.merge(stock_value, stock_indicators, on='papel')

# Recording the dataframe - Removing the duplicates
stock_dataframe.drop_duplicates('papel').to_csv('./source/DataFrame.csv', index=False, sep=";")

# Removing the csv
os.remove('./source/Stocks.csv') 
