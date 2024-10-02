## ETL Project: Top 10 Largest Banks by Market Capitalization
#### Project Overview
This project involves building an automated ETL (Extract, Transform, Load) pipeline to extract and process the list of the top 10 largest banks in the world ranked by market capitalization from a given webpage.  
Additionally, the market capitalization (MC) values will be converted into multiple currencies (USD, GBP, EUR, and INR) based on exchange rates provided in a CSV file named exchange_rate.csv.

#### The final data will be:
Saved as a CSV file (Largest_banks_data.csv) for local storage.  
Loaded into a SQLite database (Banks.db) with a table named Largest_banks for querying.  
Queries will be performed to extract the market capitalization in different currencies for specific country offices.  
Additionally, the script will log the process execution in a file named code_log.txt.

#### Key Features 
***Data Extraction***: The script extracts the list of the top 10 largest banks by market capitalization from the webpage.<br>
***Data Transformation***: The script transforms the data by converting the market capitalization values into GBP, EUR, and INR based on the exchange rate provided in a CSV file. All values are rounded to 2 decimal places.<br>
***Data Loading***:   
CSV: The transformed data is saved as a CSV file.   
SQLite Database: The transformed data is also loaded into a SQLite database table.<br>
***Database Queries***: The script can run specific queries to extract market capitalization for different offices (London, Berlin, and New Delhi).  
***Logging***: Each step of the process is logged to ensure transparency and debugging capabilities.
