from __future__ import annotations
import json
import socket
from pathlib import Path

import requests
from psycopg import connect
from pymongo import MongoClient

from extractor.json_extractor import JsonExtractor
from parser.vehicle_parser import VehicleParser
from transformer.vehicle_mapper import VehicleMapper
from validator.schema_validator import SchemaValidator
from loader.postgres_loader import PostgresLoader
from loader.mongo_loader import MongoLoader

vin = "1HGCM82633A004352"
url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{vin}?format=json"

print("=== STEP 1: Fetch real VIN source ===")
resp = requests.get(url, timeout=30)
resp.raise_for_status()
body = resp.json()
record = (body.get("Results") or [{}])[0]
raw_vehicle = {
    "vin": vin,
    "make": record.get("Make"),
    "model": record.get("Model"),
    "modelYear": record.get("ModelYear"),
    "engine": record.get("EngineModel") or record.get("EngineConfiguration"),
    "source": "vpic_nhtsa"
}
print("Fetched:", raw_vehicle)

print("\n=== STEP 2: Save & parse 1 real auto file ===")
demo_dir = Path("demo_data")
demo_dir.mkdir(exist_ok=True)
json_file = demo_dir / "vehicle_vin_real.json"
json_file.write_text(json.dumps(raw_vehicle, ensure_ascii=False, indent=2), encoding="utf-8")
print("Saved file:", json_file)

raw_text = json_file.read_text(encoding="utf-8")
extracted = JsonExtractor().extract(raw_text)
parsed = VehicleParser().parse(extracted)
mapped = VehicleMapper().map(parsed)
validated = SchemaValidator().validate("vehicle", mapped)

print("Parsed:", parsed)
print("Mapped:", mapped)
print("Validated:", validated)

print("\n=== STEP 3: Loader dry-run check ===")
pg = PostgresLoader()
mg = MongoLoader()
print("PostgresLoader:", pg.save("vehicles", validated))
print("MongoLoader:", mg.save("vehicles", validated))

print("\n=== STEP 4: DB connectivity check (localhost) ===")

def check_port(host: str, port: int) -> str:
    try:
        with socket.create_connection((host, port), timeout=2):
            return "OPEN"
    except OSError as exc:
        return f"CLOSED ({exc})"

print("PostgreSQL 5432:", check_port("localhost", 5432))
print("MongoDB 27017:", check_port("localhost", 27017))

try:
    with connect("host=localhost port=5432 dbname=autocare_pipeline user=postgres password=postgres connect_timeout=3") as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
            print("PostgreSQL query: OK", cur.fetchone())
except Exception as exc:
    print("PostgreSQL query: FAIL", exc)

try:
    mc = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=3000)
    pong = mc.admin.command("ping")
    print("MongoDB ping: OK", pong)
except Exception as exc:
    print("MongoDB ping: FAIL", exc)
