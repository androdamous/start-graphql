import strawberry
from typing import List, Optional
from datetime import date
import sqlite3

# Database connection
def get_db_connection():
    conn = sqlite3.connect("telematics.db")
    conn.row_factory = sqlite3.Row
    return conn

# Data Models
@strawberry.type
class HealthReport:
    fuel: float
    distance: float
    time_period: str

@strawberry.type
class Vehicle:
    name: str
    health_report: HealthReport

# Helper function to fetch vehicle data
def fetch_vehicle_health(v_id: Optional[int] = None, time_period: str = "daily") -> List[Vehicle]:
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Define time aggregation
    time_filter = {
        "daily": "strftime('%Y-%m-%d', d.full_date)",
        "weekly": "strftime('%Y-%W', d.full_date)",
        "monthly": "strftime('%Y-%m', d.full_date)"
    }.get(time_period, "strftime('%Y-%m-%d', d.full_date)")
    
    query = f'''
    SELECT v.v_name, AVG(f.fuel_level) AS avg_fuel, SUM(f.distance) AS total_distance
    FROM fact_vehicle_metrics f
    JOIN dim_vehicle v ON f.dim_vehicle_key = v.dim_vehicle_key
    JOIN dim_date d ON f.dim_date_key = d.dim_date_key
    WHERE 1=1
    '''
    
    params = []
    if v_id:
        query += " AND v.v_id = ?"
        params.append(v_id)
    
    query += f" GROUP BY v.v_name, {time_filter}"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    return [
        Vehicle(
            name=row["v_name"],
            health_report=HealthReport(
                fuel=row["avg_fuel"],
                distance=row["total_distance"],
                time_period=time_period
            )
        )
        for row in rows
    ]

# GraphQL Schema
@strawberry.type
class Query:
    @strawberry.field
    def vehicle(self, v_id: Optional[int] = None, time_period: str = "daily") -> List[Vehicle]:
        return fetch_vehicle_health(v_id, time_period)

schema = strawberry.Schema(query=Query)
