import sqlite3
from datetime import datetime, timedelta
import random

# Connect to SQLite database
conn = sqlite3.connect("telematics.db")
cursor = conn.cursor()

# Create Dimension Tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_vehicle (
    dim_vehicle_key INTEGER PRIMARY KEY AUTOINCREMENT,
    v_id INTEGER UNIQUE,
    v_name TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS dim_date (
    dim_date_key INTEGER PRIMARY KEY AUTOINCREMENT,
    full_date DATE UNIQUE,
    day INTEGER,
    month INTEGER,
    year INTEGER,
    quarter INTEGER,
    week_of_year INTEGER
);
""")

# Create Fact Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS fact_vehicle_metrics (
    fact_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dim_vehicle_key INTEGER,
    dim_date_key INTEGER,
    fuel_level SMALLINT,
    distance FLOAT,
    FOREIGN KEY (dim_vehicle_key) REFERENCES dim_vehicle(dim_vehicle_key),
    FOREIGN KEY (dim_date_key) REFERENCES dim_date(dim_date_key)
);
""")

# Insert sample vehicles
dim_vehicles = [
    (1, "Duc Terra V"),
    (2, "Thang's EcoSport"),
    (3, "Dung BJX7"),
    (4, "SH's Car"),
    (5, "KK"),
    (6, "Haibeo"),
    (7, "Mazda Cx3"),
    (8, "Fortuner")
]
cursor.executemany("INSERT OR IGNORE INTO dim_vehicle (v_id, v_name) VALUES (?, ?)", dim_vehicles)

# Insert sample date records (last 30 days)
dim_dates = [(i, (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')) for i in range(30)]
cursor.executemany("INSERT OR IGNORE INTO dim_date (dim_date_key, full_date) VALUES (?, ?)", dim_dates)

# Insert sample fact records
fact_records = []
for vehicle in dim_vehicles:
    for date in dim_dates:
        fact_records.append((
            vehicle[0],  # dim_vehicle_key
            date[0],     # dim_date_key
            random.randint(10, 100),  # fuel_level (random 10%-100%)
            round(random.uniform(5, 200), 2)  # distance (5-200 km)
        ))

cursor.executemany("""
INSERT INTO fact_vehicle_metrics (dim_vehicle_key, dim_date_key, fuel_level, distance)
VALUES (?, ?, ?, ?)""", fact_records)

# Commit and close
conn.commit()
conn.close()

print("Sample data inserted successfully!")