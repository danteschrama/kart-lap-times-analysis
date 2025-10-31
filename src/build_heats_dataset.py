import json
import os
from pathlib import Path

import pandas as pd

base_path = Path("data")

records = []

for location_dir in base_path.iterdir():
    if not location_dir.is_dir():
        continue
    location = location_dir.name

    for year_dir in location_dir.iterdir():
        if not year_dir.is_dir():
            continue
        year = year_dir.name

        for month_dir in year_dir.iterdir():
            if not month_dir.is_dir():
                continue
            month = month_dir.name

            for json_file in month_dir.glob("*.json"):
                day = json_file.stem  # e.g. "01"
                with open(json_file, "r") as f:
                    data = json.load(f)

                # Assume data is a list of heats
                for heat in data:
                    heat["location"] = location
                    heat["year"] = year
                    heat["month"] = month
                    heat["day"] = day
                    records.append(heat)

# Convert to DataFrame
df = pd.DataFrame(records)

# Save
df.to_csv("all_heats.csv", index=False)
df.to_parquet("all_heats.parquet", index=False)
