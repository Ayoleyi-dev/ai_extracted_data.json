# An Automated JSON Invoice Validator

## Overview
A lightweight QA pipeline that validates AI-extracted document data. Simulates real-world enterprise data cleaning by performing field-level validation, type enforcement, and mathematical reconciliation on JSON invoice dumps.

##  What It Checks
- **Null/Missing Fields:** Flags empty or missing critical metadata
- **Data Type Enforcement:** Catches strings where numerics/dates are expected
- **Line-Item Math:** Verifies `quantity × unit_price == line_total` (with float tolerance)
- **Total Reconciliation:** Ensures sum of line items matches `invoice_total`

## Stack
- Python 3.x
- Standard Libraries: `json`, `csv`, `datetime` (Zero external dependencies)

## How to Run
1. Place `ai_extracted_data.json` and `validator.py` in the same directory.
2. Run: `python validator.py`
3. Review the generated `validation_report.csv` for the structured error log.

##  Sample Output
| invoice_id | category | issue                                      |
|------------|----------|--------------------------------------------|
| INV-001    | VALID    | Passed all checks                          |
| INV-002    | FLAGGED  | Missing/Empty required field: 'date'       |
| INV-002    | FLAGGED  | Design Work: Invalid type for 'quantity'   |
| INV-003    | FLAGGED  | Missing/Empty required field: 'client_name'|
| INV-003    | FLAGGED  | Invoice total mismatch. Expected 500.00... |
