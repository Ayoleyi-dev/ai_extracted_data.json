import json
import csv
from datetime import datetime

def load_json(filepath):
    """Load and return JSON data from a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def validate_invoices(invoices):
    """Run field, type, and math validation. Returns a list of error/valid records."""
    report = []
    
    for inv in invoices:
        inv_id = inv.get("invoice_id", "UNKNOWN")
        inv_errors = []
        
        # 1. Null / Missing Field Check
        for field in ["date", "client_name"]:
            val = inv.get(field)
            if val is None or (isinstance(val, str) and val.strip() == ""):
                inv_errors.append(f"Missing/Empty required field: '{field}'")
                
        # 2. Date Format Check
        date_val = inv.get("date")
        if date_val and isinstance(date_val, str):
            try:
                datetime.strptime(date_val, "%Y-%m-%d")
            except ValueError:
                inv_errors.append(f"Invalid date format: '{date_val}'")
        elif date_val and not isinstance(date_val, str):
            inv_errors.append(f"Expected string for 'date', got {type(date_val).__name__}")
            
        # 3. Line Items Validation
        line_items = inv.get("line_items", [])
        if not isinstance(line_items, list):
            inv_errors.append("'line_items' is not a list")
            line_items = []
            
        calculated_sum = 0.0
        for i, item in enumerate(line_items):
            item_name = item.get("item", f"Item_{i}")
            qty = item.get("quantity")
            price = item.get("unit_price")
            
            # Type enforcement
            if not isinstance(qty, (int, float)):
                inv_errors.append(f"{item_name}: Invalid type for 'quantity' (expected number, got {type(qty).__name__})")
                continue
            if not isinstance(price, (int, float)):
                inv_errors.append(f"{item_name}: Invalid type for 'unit_price' (expected number, got {type(price).__name__})")
                continue
                
            # Line math check
            expected_line_total = qty * price
            actual_line_total = item.get("line_total")
            
            if not isinstance(actual_line_total, (int, float)):
                inv_errors.append(f"{item_name}: Invalid type for 'line_total'")
                continue
                
            if abs(actual_line_total - expected_line_total) > 0.01:
                inv_errors.append(f"{item_name}: Math mismatch. Expected {expected_line_total:.2f}, got {actual_line_total}")
                
            calculated_sum += actual_line_total
            
        # 4. Invoice Total Reconciliation
        invoice_total = inv.get("invoice_total")
        if isinstance(invoice_total, (int, float)):
            if abs(invoice_total - calculated_sum) > 0.01:
                inv_errors.append(f"Invoice total mismatch. Expected {calculated_sum:.2f}, got {invoice_total}")
        
        # Log results
        if inv_errors:
            for err in inv_errors:
                report.append({"invoice_id": inv_id, "category": "FLAGGED", "issue": err})
        else:
            report.append({"invoice_id": inv_id, "category": "VALID", "issue": "Passed all checks"})
            
    return report

def save_report(report, output_path):
    """Export validation report to CSV."""
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["invoice_id", "category", "issue"])
        writer.writeheader()
        writer.writerows(report)

if __name__ == "__main__":
    INPUT_FILE = "ai_extracted_data.json"
    OUTPUT_FILE = "validation_report.csv"
    
    print(" Loading JSON data...")
    try:
        data = load_json(INPUT_FILE)
    except Exception as e:
        print(f" Failed to load JSON: {e}")
        exit(1)
        
    print(" Running validation pipeline...")
    report = validate_invoices(data)
    
    save_report(report, OUTPUT_FILE)
    
    valid = sum(1 for r in report if r["category"] == "VALID")
    flagged = sum(1 for r in report if r["category"] == "FLAGGED")
    print(f" VALID: {valid} |  FLAGGED: {flagged}")
    print(f" Report saved to: {OUTPUT_FILE}")
