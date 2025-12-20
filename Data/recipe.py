import json
import math

json_file = r"US_recipes_null.Pdf.json"
output_file = r"parsed_Data.json"

def numeric_fields(value):
    try:
        if value is None:
            return None
        v = float(value)
        if math.isnan(v):
            return None
        return v
    except (ValueError, TypeError):
        return None

with open(json_file, "r", encoding="utf-8") as parse:
    data = json.load(parse)

for _, recipe in data.items():
    for field in ["rating", "prep_time", "cook_time", "total_time"]:
        if field in recipe:
            recipe[field] = numeric_fields(recipe.get(field))

with open(output_file, "w", encoding="utf-8") as out:
    json.dump(data, out, indent=4)
