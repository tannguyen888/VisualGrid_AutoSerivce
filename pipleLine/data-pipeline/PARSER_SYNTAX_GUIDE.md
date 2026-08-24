# Parser Syntax Guide (AutoCare ETL)

Tai lieu nay gom tat ca syntax va pattern can thiet de ban tu xay parser trong pipeline nay.

## 1) Tong quan luong du lieu

```text
Source -> Extractor -> Parser -> Mapper -> SchemaValidator -> DataQualityValidator -> Loader
```

- Source: lay du lieu tho tu API/file.
- Extractor: chuyen raw payload (json/xml/pdf/html) thanh object co the parse.
- Parser: boc tach truong nghiep vu.
- Mapper: chuan hoa ve canonical schema.
- Validator: kiem tra schema + quality.
- Loader: luu vao Postgres/Mongo/Storage.

## 2) Syntax Python cot loi ban can

### 2.1 Type hints

```python
from typing import Any

def parse(self, raw_data: dict[str, Any]) -> dict[str, Any]:
    ...
```

### 2.2 Alias key + fallback

```python
value = raw_data.get("oem_number") or raw_data.get("oemNumber") or ""
```

### 2.3 Chuan hoa string

```python
vin = str(raw_data.get("vin") or "").strip().upper() or None
make = str(raw_data.get("make") or "").strip().title()
```

### 2.4 Xu ly list/chuoi linh hoat

```python
compatibility = raw_data.get("compatibility") or []
if isinstance(compatibility, str):
    compatibility = [x.strip() for x in compatibility.split(",") if x.strip()]
```

### 2.5 Regex extract

```python
import re
TORQUE_PATTERN = re.compile(r"\b\d+(?:\.\d+)?\s*(?:Nm|N\.m|lb-ft)\b", re.IGNORECASE)
torque_values = TORQUE_PATTERN.findall(text)
```

### 2.6 Error handling

```python
try:
    payload = source.fetch(vin=vin)
except Exception as exc:
    logger.exception("Source fetch failed: %s", exc)
```

## 3) Template Source

```python
from __future__ import annotations
from typing import Any
from sources.base_source import BaseSource

class VinSource(BaseSource):
    def fetch(self, **kwargs: Any) -> dict[str, Any]:
        vin = str(kwargs.get("vin", "")).strip().upper()
        if not vin:
            raise ValueError("vin is required")
        return self._request_json(path="vin/decode", params={"vin": vin})
```

## 4) Template Extractor

### 4.1 JSON Extractor

```python
import json
from typing import Any

class JsonExtractor:
    def extract(self, raw_json: str | bytes | dict[str, Any] | list[Any]) -> dict[str, Any] | list[Any]:
        if isinstance(raw_json, (dict, list)):
            return raw_json
        if isinstance(raw_json, bytes):
            raw_json = raw_json.decode("utf-8", errors="replace")
        if not raw_json:
            return {}
        return json.loads(raw_json)
```

### 4.2 XML Extractor (mau)

```python
import xml.etree.ElementTree as ET

class XmlExtractor:
    def extract(self, xml_text: str | bytes) -> dict:
        if isinstance(xml_text, bytes):
            xml_text = xml_text.decode("utf-8", errors="replace")
        root = ET.fromstring(xml_text)
        return {"tag": root.tag, "attributes": dict(root.attrib)}
```

## 5) Template Parser

Parser chi lam 1 viec: boc tach semantic field, KHONG validate schema tai day.

```python
from __future__ import annotations

class VehicleParser:
    def parse(self, raw_data: dict) -> dict:
        return {
            "vin": raw_data.get("vin") or raw_data.get("VIN"),
            "make": raw_data.get("make") or raw_data.get("manufacturer") or "",
            "model": raw_data.get("model") or raw_data.get("vehicleModel") or "",
            "year": raw_data.get("year") or raw_data.get("modelYear") or 0,
            "engine": raw_data.get("engine") or raw_data.get("engineType"),
            "source": raw_data.get("source", "vehicle_provider"),
        }
```

### Rule parser de de bao tri

- Chi parse + alias key, khong goi DB.
- Luon tra ve dict shape on dinh.
- Gan source mac dinh neu thieu.
- Khong throw error voi field optional.

## 6) Template Mapper

Mapper bien parse output thanh canonical shape de validate.

```python
class VehicleMapper:
    def map(self, vehicle_data: dict) -> dict:
        return {
            "vin": str(vehicle_data.get("vin") or "").strip().upper() or None,
            "make": str(vehicle_data.get("make") or "").strip().title(),
            "model": str(vehicle_data.get("model") or "").strip(),
            "year": int(vehicle_data.get("year") or 0),
            "engine": vehicle_data.get("engine"),
            "source": vehicle_data.get("source", "unknown"),
        }
```

## 7) Template Schema (Pydantic)

```python
from pydantic import BaseModel, Field, field_validator

class VehicleSchema(BaseModel):
    vin: str | None = Field(default=None, min_length=11, max_length=17)
    make: str = Field(min_length=1)
    model: str = Field(min_length=1)
    year: int = Field(ge=1950, le=2100)
    engine: str | None = None
    source: str = Field(default="unknown")

    @field_validator("vin")
    @classmethod
    def normalize_vin(cls, value: str | None) -> str | None:
        if value is None:
            return value
        cleaned = value.strip().upper()
        return cleaned or None
```

## 8) Schema Validator + Data Quality

```python
from pydantic import ValidationError

class SchemaValidator:
    def validate(self, model_cls, payload: dict) -> dict:
        try:
            return model_cls.model_validate(payload).model_dump()
        except ValidationError as exc:
            raise ValueError(f"Schema validation failed: {exc}") from exc
```

```python
class DataQualityValidator:
    def check(self, payload: dict, required_fields: list[str]) -> tuple[bool, list[str]]:
        issues = []
        for field in required_fields:
            value = payload.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                issues.append(f"missing required field: {field}")
        return (len(issues) == 0, issues)
```

## 9) Loader syntax

### 9.1 Postgres (SQLAlchemy text)

```python
from sqlalchemy import create_engine, text

engine = create_engine(database_url)
query = text("INSERT INTO vehicles (vin, make, model, year) VALUES (:vin, :make, :model, :year)")
with engine.begin() as conn:
    conn.execute(query, {"vin": "...", "make": "...", "model": "...", "year": 2003})
```

### 9.2 Mongo

```python
from pymongo import MongoClient

client = MongoClient(mongodb_url)
result = client["autocare"]["vehicles"].insert_one(payload)
print(result.inserted_id)
```

### 9.3 Dry-run pattern

```python
if self.dry_run:
    return {"status": "dry-run", "payload": payload}
```

## 10) End-to-end mini orchestrator

```python
raw = source.fetch(vin="1HGCM82633A004352")
extracted = JsonExtractor().extract(raw)
parsed = VehicleParser().parse(extracted)
mapped = VehicleMapper().map(parsed)
validated = SchemaValidator().validate(VehicleSchema, mapped)
quality_ok, issues = DataQualityValidator().check(validated, ["make", "model", "year"])
if quality_ok:
    PostgresLoader().save("vehicles", validated)
```

## 11) Checklist khi tao parser moi

1. Dinh nghia input shape tu provider (co sample JSON/XML).
2. Viet parser alias key + fallback + default.
3. Viet mapper chuan hoa kieu du lieu.
4. Viet schema Pydantic cho entity moi.
5. Dang ky vao SchemaValidator.
6. Them data quality rule can thiet.
7. Test voi 1 payload that + 1 payload loi.

## 12) Loi thuong gap va cach fix

- year la string: cast `int(...)` trong mapper.
- key doi ten theo provider: dung chain `or`.
- payload rong: return dict default an toan.
- parser qua nhieu logic: tach qua extractor/parser/mapper cho de test.
- fail import dependency: uu tien standard library neu co the.

## 13) Lenh test nhanh parser

```powershell
c:/project/java/HọcBackend/AutoCare/.venv/Scripts/python.exe -c "from parser.vehicle_parser import VehicleParser; print(VehicleParser().parse({'VIN':'1HG','manufacturer':'HONDA','vehicleModel':'Accord','modelYear':'2003'}))"
```

## 14) Ban do file trong project nay (de hoc nhanh)

- Source: sources/
- Extractor: extractor/
- Parser: parser/
- Mapper: transformer/
- Schema: models/
- Validation: validator/
- Load: loader/
- Orchestrator: main.py

Ban co the bat dau clone theo cap: `part_parser.py + part_mapper.py + part_schema.py` de tao entity moi nhanh nhat.
