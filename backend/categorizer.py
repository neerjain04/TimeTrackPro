import csv
import json
import os

def categorize_sessions():
    # Load app-to-category mappings
    with open("app_categories.json", "r") as f:
        category_map = json.load(f)

    # File paths
    input_file = os.path.join("data", "usage_log.csv")
    output_file = os.path.join("data", "labeled_log.csv")

    # Read the original log and write a new labeled one
    with open(input_file, "r", encoding="utf-8") as infile, \
         open(output_file, "w", newline="", encoding="utf-8") as outfile:
        
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ["Category"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            process_name = row["Process Name"]
            category = category_map.get(process_name, "unknown")
            row["Category"] = category
            writer.writerow(row)

    print("Categorization complete → data/labeled_log.csv")
