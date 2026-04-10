#  AI Document Extraction QA & Annotation Validator

## Overview
A lightweight validation pipeline built to mirror enterprise document annotation workflows. Simulates the review of AI-extracted JSON against source documents by performing field-by-field validation, verifying mathematical accuracy of line-item totals, and flagging schema/type discrepancies for manual correction.

##  Validation Checks (Mapped to Role Requirements)
- **JSON Schema & Field Compliance:** Flags missing, null, or empty required fields
- **Data Type Enforcement:** Catches string/numeric mismatches (e.g., `"quantity": "five"`)
- **Mathematical Accuracy:** Verifies `quantity × unit_price == line_total` with float tolerance
- **Invoice Reconciliation:** Cross-checks line-item sums against `invoice_total`
- **Error Logging:** Outputs a structured, annotation-ready CSV for rapid review & escalation

##  Tech Stack
- Python 3.x (Standard libraries only: `json`, `csv`, `datetime`)
- Zero external dependencies → easily reproducible & lightweight

## How to Run
1. Ensure `ai_extracted_data.json` and `validator.py` are in the same directory
2. Run: `python validator.py`
3. Review `validation_report.csv` for field-level error logs

##  Why This Matters for Document Annotation
This project demonstrates a working understanding of:
- How AI extraction pipelines fail in production
- The exact validation steps needed before human-in-the-loop annotation
- How to systematically document edge cases, math errors, and schema mismatches
- Translating manual QA workflows into repeatable, auditable processes
