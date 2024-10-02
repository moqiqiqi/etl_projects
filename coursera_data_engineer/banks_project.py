# Code for ETL operations on Country-GDP data
# Importing the required libraries
import sqlite3
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

url = 'https://web.archive.org/web/20230908091635/https://en.wikipedia.org/wiki/List_of_largest_banks'
table_attribs=['Name', 'MC_USD_Billion']
output_path = 'Largest_banks_data.csv'
csv_path = './exchange_rate.csv'
db_name = 'Banks.db'
table_name = 'Largest_banks'


def log_progress(message):
    ''' This function logs the mentioned message of a given stage of the
    code execution to a log file. Function returns nothing'''
    now=datetime.now()
    time_foramt='%Y-%h-%d-%H:%M:%S'
    timestamp=now.strftime(time_foramt)
    with open("code_log.txt", 'a') as f:
        f.write(timestamp+':'+message+'\n')


def extract(url, table_attribs):
    ''' This function aims to extract the required
    information from the website and save it to a data frame. The
    function returns the data frame for further processing. '''
    page = requests.get(url).text
    data = BeautifulSoup(page,'html.parser')
    tables = data.find_all('tbody')
    rows = tables[0].find_all('tr')
    df = pd.DataFrame(columns=table_attribs)
    for row in rows:
        col = row.find_all('td')
        if len(col) != 0:
            data_dict = {table_attribs[0]: col[1].contents[2].text,
                    table_attribs[1]: float(col[2].text[:-1])} 
            df = pd.concat([df, pd.DataFrame([data_dict])], ignore_index=True)
    return df

def transform(df, csv_path):
    ''' This function accesses the CSV file for exchange rate
    information, and adds three columns to the data frame, each
    containing the transformed version of Market Cap column to
    respective currencies'''
    dataframe = pd.read_csv(csv_path)
    exchange_rate = dataframe.set_index('Currency').to_dict()['Rate']
    df['MC_GBP_Billion'] = [np.round(x*exchange_rate['GBP'],2) for x in df['MC_USD_Billion']]
    df['MC_EUR_Billion'] = np.round(df['MC_USD_Billion']*exchange_rate['EUR'],2)
    df['MC_INR_Billion'] = round(df['MC_USD_Billion']*exchange_rate['INR'],2)
    return df

def load_to_csv(df, output_path):
    ''' This function saves the final data frame as a CSV file in
    the provided path. Function returns nothing.'''
    df.to_csv(output_path)

def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final data frame to a database
    table with the provided name. Function returns nothing.'''
    df.to_sql(table_name,sql_connection, if_exists='replace', index=False)

def run_query(query_statement, sql_connection):
    ''' This function runs the query on the database table and
    prints the output on the terminal. Function returns nothing. '''
    print(query_statement)
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_output)

''' 
Here, you define the required entities and call the relevant functions in the correct order 
to complete the project. 
Note that this portion is not inside any function.
'''

log_progress("Preliminaries complete. Initiating ETL process")

df=extract(url, table_attribs)
# print(df)
log_progress("Data extraction complete. Initiating Transformation process")

df=transform(df, csv_path)
# print(df)
log_progress("Data transformation complete. Initiating Loading process")

print(df['MC_EUR_Billion'][4])

load_to_csv(df, output_path)
log_progress("Data saved to CSV file")

sql_connection=sqlite3.connect(db_name)
log_progress("SQL Connection initiated")

load_to_db(df, sql_connection, table_name)
log_progress("Data loaded to Database as a table, Executing queries")

run_query("SELECT * FROM Largest_banks", sql_connection)
run_query("SELECT AVG(MC_GBP_Billion) FROM Largest_banks", sql_connection)
run_query("SELECT Name from Largest_banks LIMIT 5", sql_connection)
log_progress("Process Complete")

sql_connection.close()
log_progress("Server Connection closed")
