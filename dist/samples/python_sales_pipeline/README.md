# Python Sales Data Quality Pipeline

This independent practice project uses synthetic sales records to demonstrate a small, reviewable data preparation workflow with Python and pandas.

## What the script does

1. Reads the source CSV without changing it.
2. Trims and standardises transaction IDs, customer names, product names and region labels.
3. Parses mixed date formats, quantities and South African Rand amounts.
4. Checks for missing or duplicate IDs, invalid dates, missing customers, unmapped regions, non-positive quantities and invalid or negative amounts.
5. Writes accepted records, rejected records and a JSON quality summary to `outputs/`.

The script keeps every rejected row and its issue flags for review. It does not silently discard exceptions. The sample assumes commas in Rand values are thousands separators and a period is the decimal separator.

## Run it

Use Python 3.10 or later. From this folder, install the listed dependency and run:

```text
python -m pip install -r requirements.txt
python clean_sales_data.py
```

Generated files:

- `outputs/sales_cleaned.csv`
- `outputs/sales_exceptions.csv`
- `outputs/quality_summary.json`

## Data note

All customer names, transactions and amounts are synthetic. The data is for demonstration and does not describe a real business or customer.
