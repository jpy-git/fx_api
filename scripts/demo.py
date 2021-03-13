# Script specific imports
import os
import sqlite3
from sqlalchemy import create_engine
import pandas as pd

# API import
from fx_api import FX

# Query API
FX_df = FX(source_currency=["GBP", "USD", "EUR"]).get_FX_date_range(start_at="2018-01-01", end_at="2021-01-01")

# Save query to CSV
script_location = os.path.dirname(__file__)
csv_path = os.path.join(script_location, "exchange_rates.csv")
FX_df.to_csv(
    csv_path,
    index=False
)

# Create SQLLite database and add exchange_rates table
sqlite_path = os.path.join(script_location, "exchange_rates.sqlite3")
con = sqlite3.connect(sqlite_path)

cur = con.cursor()

drop_existing_exchange_rates_sql = """
DROP TABLE IF EXISTS exchange_rates
"""
cur.execute(drop_existing_exchange_rates_sql)

exchange_rates_sql = """
CREATE TABLE exchange_rates (
    id integer PRIMARY KEY,
    date text NOT NULL,
    source_currency text NOT NULL,
    target_currency text NOT NULL,
    exchange_rate_to_target real NOT NULL
);
"""
cur.execute(exchange_rates_sql)

# Import CSV and load to SQLLite database
imported_FX_df = pd.read_csv(
    csv_path
)

engine = create_engine(
    f"sqlite:///{sqlite_path}"
)
upload_con = engine.connect()

imported_FX_df.to_sql(
    "exchange_rates",
    con=upload_con,
    if_exists="append",
    index=False
)

# Query SQLLite database
exchange_rate_query_sql = """
SELECT *
FROM exchange_rates
"""
sql_FX_df = pd.read_sql(
    exchange_rate_query_sql,
    con=con
)

print(sql_FX_df.head(5))




