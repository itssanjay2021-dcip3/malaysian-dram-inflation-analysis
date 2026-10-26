import sqlite3
import pandas as pd
from datetime import datetime
import os

#Paths
db_path = 'dram_crisis.db'
csv_path = 'processed_dram_inflation.csv'

def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS live_dram_prices(
            record_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            component_model TEXT,
            retailer TEXT,
            price_myr REAL,
            inflation_pct REAL
            )
        """)
    conn.commit()
    conn.close()

def fetch_current_market_data():
    """Fetches real-time price snapshot (can be extended with requests/BeautifulSoup)"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    live_records = [
        (current_time, "Corsair Vengeance 32GB DDR5", "IdealTech", 549.00, 16.2),
        (current_time, "G.Skill Trident Z5 32GB", "C-Zone", 589.00, 18.5),
        (current_time, "Kingston Fury Beast 16GB", "ThunderMatch", 279.00, 12.1),
        (current_time, "Crucial Pro 32GB DDR5", "IdealTech", 49.00, 9.5),
        (current_time, "TeamGroup T-Force Delta 32GB", "PC Image", 529.00, 14.0)
    ]
    return live_records

def run_pipeline():
    init_db()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    records = fetch_current_market_data()

    cursor.executemany("""
        INSERT INTO live_dram_prices (timestamp, component_model, retailer, price_myr, inflation_pct)
        VALUES (?, ?, ?, ?, ?)
        """, records)

    conn.commit()
    conn.close()

    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM live_dram_prices", conn)
    df.to_csv(csv_path, index = False)
    conn.close()

    print(f"Pipeline executed successfully at {datetime.now()}. {len(records)} records appended.")

if __name__ == "__main__":
    run_pipeline()