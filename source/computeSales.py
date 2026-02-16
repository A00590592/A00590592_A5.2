import json
import os
import sys
import time

def get_results_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(current_dir, "..", "results")
    output_name = "SalesResults.txt"

    if os.path.isdir(results_dir):
        return os.path.join(results_dir, output_name)

    return output_name


def load_json_file(file_path):
    """Loads a JSON file and returns the parsed content or None."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as error:
        print(f"Error reading JSON -> {file_path}: {error}")
        return None


def build_price_catalog(price_data):
    """Builds a dictionary mapping product title to price."""
    catalog = {}

    if not isinstance(price_data, list):
        print("Error: Price catalogue must be a list.")
        return catalog

    for item in price_data:
        if not isinstance(item, dict):
            continue

        title = item.get("title")
        price = item.get("price")

        if isinstance(title, str) and isinstance(price, (int, float)):
            catalog[title] = float(price)

    return catalog


def main():
    if len(sys.argv) != 3:
        print("Usage: python computeSales.py priceCatalogue.json salesRecord.json")
        return

    price_file = sys.argv[1]
    sales_file = sys.argv[2]

    if not os.path.isfile(price_file):
        print(f"Error: file not found -> {price_file}")
        return

    if not os.path.isfile(sales_file):
        print(f"Error: file not found -> {sales_file}")
        return

    price_data = load_json_file(price_file)
    sales_data = load_json_file(sales_file)

    if price_data is None or sales_data is None:
        return

    catalog = build_price_catalog(price_data)

    print("CHECKPOINT: JSON files loaded successfully")
    print(f"CHECKPOINT: price items loaded -> {len(price_data)}")
    print(f"CHECKPOINT: sales items loaded -> {len(sales_data)}")
    print(f"CHECKPOINT: Catalog created with {len(catalog)} entries")
    print(f"Sample product from catalog -> {list(catalog.items())[:3]}")
    
    
if __name__ == "__main__":
    main()