import json
import os
import sys
import time

def get_results_path(input_file):
    """Builds the output file path inside the results folder.
       The output file name is based on the input sales file name."""
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(current_dir, "..", "results")

    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)

    input_name = os.path.basename(input_file)
    base_name, _ = os.path.splitext(input_name)

    result_file = f"{base_name}_Results.txt"
    return os.path.join(results_dir, result_file)


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


def compute_total_sales(sales_data, catalog):
    """Calculates total sales and counts ignored sales records."""
    total = 0.0
    ignored = 0

    if not isinstance(sales_data, list):
        print("Error: Sales record must be a list.")
        return total, ignored

    for sale in sales_data:
        if not isinstance(sale, dict):
            ignored += 1
            continue

        product = sale.get("Product", sale.get("title"))
        quantity = sale.get("Quantity", sale.get("quantity"))

        if not isinstance(product, str):
            ignored += 1
            continue

        if isinstance(quantity, str):
            try:
                quantity = float(quantity)
            except ValueError:
                ignored += 1
                continue

        if product in catalog and isinstance(quantity, (int, float)):
            total += catalog[product] * float(quantity)
        else:
            ignored += 1

    return total, ignored


def main():
    start_time = time.time()

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

    total_sales, ignored = compute_total_sales(sales_data, catalog)
    elapsed_time = time.time() - start_time

    print()
    print("CHECKPOINT: JSON files loaded successfully")
    print(f"CHECKPOINT: price items loaded -> {len(price_data)}")
    print(f"CHECKPOINT: sales items loaded -> {len(sales_data)}")
    print(f"CHECKPOINT: Catalog created with {len(catalog)} entries")

    print("\nCOMPUTE SALES RESULTS")
    print(f"TOTAL_COST\t{total_sales:.2f}")
    print(f"IGNORED_SALES\t{ignored}")
    print(f"TIME_ELAPSED_SECONDS\t{elapsed_time:.6f}")
    print()

    output_path = get_results_path(sales_file)

    with open(output_path, "w", encoding="utf-8") as output_file:
        output_file.write("COMPUTE SALES RESULTS\n")
        output_file.write(f"TOTAL_COST\t{total_sales:.2f}\n")
        output_file.write(f"IGNORED_SALES\t{ignored}\n")
        output_file.write(f"TIME_ELAPSED_SECONDS\t{elapsed_time:.6f}\n")
    
    
if __name__ == "__main__":
    main()