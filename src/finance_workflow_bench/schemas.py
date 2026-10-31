"""Fixed-case output contract and matching dependency-free validation.

The exported JSON Schema describes field types and basic bounds. The Python
validator additionally enforces dated weekly order and unique event identities.
"""
import json
import re
from datetime import date, timedelta
from pathlib import Path

OPERATING = ["receipts", "supplier_payments", "tax_payments", "other_external_payments",
             "payroll_payments", "rent_payments", "other_recurring_payments"]
CASH = ["opening_cash", "cash_before_financing", "closing_cash"]
FINANCING = ["opening_principal", "interest_paid", "credit_draw", "principal_repayment",
             "closing_principal", "credit_available"]
LIQUIDITY_AMOUNTS = ["minimum_cash_shortfall", "unfunded_cash_deficit"]
FLAGS = ["minimum_cash_breached", "unfunded_deficit"]
MONEY = OPERATING + CASH + FINANCING + LIQUIDITY_AMOUNTS
SOURCES = ["receivables.csv", "payables.csv", "recurring_expenses.csv"]
REASONS = ["outside_horizon", "internal_transfer", "zero_outstanding"]
WEEK_KEYS = ["week", "start_date", "end_date"] + MONEY + FLAGS
MAX_FORECAST_BYTES = 1_048_576
MAX_ANALYSIS_BYTES = 65_536
MAX_ANALYSIS_WORDS = 800


def object_schema(properties):
    return dict(type="object", properties=properties, required=list(properties), additionalProperties=False)


def forecast_schema():
    week = {"week": dict(type="integer", minimum=1, maximum=13),
            "start_date": dict(type="string", pattern=r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
            "end_date": dict(type="string", pattern=r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")}
    week.update({key: dict(type="string", pattern=(r"^-?[0-9]{1,16}\.[0-9]{2}$" if key in CASH else r"^[0-9]{1,16}\.[0-9]{2}$")) for key in MONEY})
    week.update({key: dict(type="boolean") for key in FLAGS})
    identity = dict(source_file=dict(type="string", enum=SOURCES), record_id=dict(type="string", minLength=1, maxLength=128))
    schema = object_schema({
        "case_id": dict(type="string", const="cash_forecast_001"),
        "currency": dict(type="string", const="USD"),
        "weeks": dict(type="array", minItems=13, maxItems=13, items=object_schema(week)),
        "exclusions": dict(type="array", maxItems=1000, items=object_schema(dict(**identity, reason=dict(type="string", enum=REASONS)))),
        "duplicates_removed": dict(type="array", maxItems=1000, items=object_schema(dict(**identity, discarded_count=dict(type="integer", minimum=1, maximum=1000000)))),
    })
    return {"$schema": "https://json-schema.org/draft/2020-12/schema", "title": "Cash Forecast 001 submission", **schema}


def validate_subset(value, schema, path="$", errors=None):
    """Validate only keywords used by forecast_schema, not arbitrary JSON Schema."""
    errors = [] if errors is None else errors
    expected = schema["type"]
    types = {"object": dict, "array": list, "string": str, "integer": int, "boolean": bool}
    if type(value) is not types[expected]:
        errors.append(dict(path=path, message=f"Expected {expected}"))
        return errors
    if "const" in schema and value != schema["const"]:
        errors.append(dict(path=path, message=f"Expected {schema['const']!r}"))
    if "enum" in schema and value not in schema["enum"]:
        errors.append(dict(path=path, message="Value outside allowed enumeration"))
    if expected == "object":
        properties = schema["properties"]
        for key in schema["required"]:
            if key not in value:
                errors.append(dict(path=f"{path}.{key}", message="Required field missing"))
        for key in value:
            if key not in properties:
                errors.append(dict(path=f"{path}.{key}", message="Unexpected field"))
            else:
                validate_subset(value[key], properties[key], f"{path}.{key}", errors)
    elif expected == "array":
        if not schema.get("minItems", 0) <= len(value) <= schema.get("maxItems", len(value)):
            errors.append(dict(path=path, message="Array length outside allowed range"))
            return errors
        for i, item in enumerate(value):
            validate_subset(item, schema["items"], f"{path}[{i}]", errors)
    elif expected == "string":
        if not schema.get("minLength", 0) <= len(value) <= schema.get("maxLength", len(value)):
            errors.append(dict(path=path, message="String length outside allowed range"))
        if "pattern" in schema and re.fullmatch(schema["pattern"], value) is None:
            errors.append(dict(path=path, message="String does not match required format"))
    elif expected == "integer":
        if not schema.get("minimum", value) <= value <= schema.get("maximum", value):
            errors.append(dict(path=path, message="Integer outside allowed range"))
    return errors


def validate_forecast(value):
    errors = validate_subset(value, forecast_schema())
    if errors:
        return errors
    for i, week in enumerate(value["weeks"]):
        start = date(2027, 1, 4) + timedelta(weeks=i)
        for field, expected in dict(week=i + 1, start_date=start.isoformat(), end_date=(start + timedelta(days=6)).isoformat()).items():
            if week[field] != expected:
                errors.append(dict(path=f"$.weeks[{i}].{field}", message=f"Expected {expected!r} in weekly order"))
    for name in ("exclusions", "duplicates_removed"):
        identities = set()
        for i, row in enumerate(value[name]):
            key = (row["source_file"], row["record_id"])
            if key in identities:
                errors.append(dict(path=f"$.{name}[{i}]", message="Repeated source_file / record_id identity"))
            identities.add(key)
    return errors


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    target = root / "schemas/forecast.schema.json"
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(forecast_schema(), indent=2) + "\n", encoding="utf-8")
    print("Forecast JSON Schema exported.")
