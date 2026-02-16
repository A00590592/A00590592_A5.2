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

    print("CHECKPOINT: JSON files loaded successfully")
    print(f"CHECKPOINT: price items loaded -> {len(price_data)}")
    print(f"CHECKPOINT: sales items loaded -> {len(sales_data)}")
    
    
if __name__ == "__main__":
    main()