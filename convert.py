import pandas as pd
import sqlite3

df = pd.read_csv(r"C:\NSC Solar\nscsolar.csv")

conn = sqlite3.connect("consumer_data.db")
df.to_sql("consumers", conn, if_exists="replace", index=False)

print("Data imported into database.")
