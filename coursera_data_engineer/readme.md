## ETL Project: Extracting Countries by GDP from IMF Data
#### Project Overview
This project involves building an automated ETL (Extract, Transform, Load) script to extract and process a list of countries by their GDP (in billion USD) from the International Monetary Fund (IMF) website. Since the IMF releases this information biannually, this code is designed to be reused whenever new data becomes available.

The script will:

Extract GDP data of countries from the IMF webpage.
Transform the data.
Load the transformed data into:
A JSON file (Countries_by_GDP.json).
A SQLite database table (Countries_by_GDP) in a database file named World_Economies.db.
Additionally, the script will log the process execution in a file named etl_project_log.txt.

