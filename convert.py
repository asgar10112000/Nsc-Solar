import pandas as pd
import sqlite3

# Load CSV and strip extra spaces from column names
df = pd.read_csv(r"C:\NSC Solar\nscsolar.csv")
df.columns = df.columns.str.strip()

# Print columns to help debug
print("Columns in CSV:", df.columns.tolist())

# Choose your corrected column names below
required_columns = [
    "Circle", "Division", "Sub-Division", "SRType", "MIStatus",  # ← Update this based on your actual CSV
    "Applicant Name", "Address", "District", "Phase", "Load"
]

# Filter only those columns
df = df[required_columns]

# Save to SQLite DB
conn = sqlite3.connect("consumer_data.db")
df.to_sql("consumers", conn, if_exists="replace", index=False)
conn.close()

print("✅ Data imported into database.")
