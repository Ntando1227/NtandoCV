"""Prepare illustrative sales CSV data for analysis.

The raw file is never overwritten. Qualified rows and rejected rows are
written to separate output files so each decision can be reviewed.
"""

from pathlib import Path
from collections import Counter
import json

import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parent
RAW_FILE = PROJECT_DIR / "sales_raw.csv"
OUTPUT_DIR = PROJECT_DIR / "outputs"

REGION_MAP = {
    "gauteng": "Gauteng",
    "gp": "Gauteng",
    "limpopo": "Limpopo",
    "western cape": "Western Cape",
    "wc": "Western Cape",
}


def clean_text(values: pd.Series) -> pd.Series:
    """Trim extra spaces and convert empty strings to missing values."""
    cleaned = values.astype("string").str.strip()
    return cleaned.replace("", pd.NA)


def parse_amount(values: pd.Series) -> pd.Series:
    """Convert South African Rand strings to numeric values.

    This sample assumes commas in amounts are thousands separators and a
    period is the decimal separator, for example ``R 1,250.50``.
    """
    text = clean_text(values)
    text = (
        text.str.replace("R", "", case=False, regex=False)
        .str.replace(" ", "", regex=False)
        .str.replace(",", "", regex=False)
    )
    return pd.to_numeric(text, errors="coerce")


def prepare_sales(raw: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Standardise records, apply quality rules and create review outputs."""
    data = raw.copy()
    data.insert(0, "source_row", range(2, len(data) + 2))

    data["transaction_id_clean"] = clean_text(data["transaction_id"]).str.upper()
    data["customer_clean"] = clean_text(data["customer"]).str.title()
    data["region_key"] = clean_text(data["region"]).str.casefold()
    data["region_clean"] = data["region_key"].map(REGION_MAP)
    data["product_clean"] = clean_text(data["product"]).str.title()
    data["order_date_clean"] = pd.to_datetime(
        clean_text(data["order_date"]),
        format="mixed",
        dayfirst=True,
        errors="coerce",
    )
    data["quantity_clean"] = pd.to_numeric(clean_text(data["quantity"]), errors="coerce")
    data["amount_clean"] = parse_amount(data["amount"])

    duplicate_id = data["transaction_id_clean"].duplicated(keep=False) & data["transaction_id_clean"].notna()
    issues_by_row = []
    for index, row in data.iterrows():
        issues = []
        if pd.isna(row["transaction_id_clean"]):
            issues.append("missing_transaction_id")
        if duplicate_id.loc[index]:
            issues.append("duplicate_transaction_id")
        if pd.isna(row["order_date_clean"]):
            issues.append("invalid_order_date")
        if pd.isna(row["customer_clean"]):
            issues.append("missing_customer")
        if pd.isna(row["region_clean"]):
            issues.append("unmapped_region")
        if pd.isna(row["quantity_clean"]) or row["quantity_clean"] <= 0:
            issues.append("invalid_quantity")
        if pd.isna(row["amount_clean"]) or row["amount_clean"] < 0:
            issues.append("invalid_amount")
        issues_by_row.append("; ".join(issues))

    data["issue_flags"] = issues_by_row
    accepted = data.loc[data["issue_flags"].eq("")].copy()
    exceptions = data.loc[data["issue_flags"].ne("")].copy()

    clean_columns = {
        "source_row": "source_row",
        "transaction_id_clean": "transaction_id",
        "order_date_clean": "order_date",
        "customer_clean": "customer",
        "region_clean": "region",
        "product_clean": "product",
        "quantity_clean": "quantity",
        "amount_clean": "sales_amount_zar",
    }
    cleaned_output = accepted[list(clean_columns)].rename(columns=clean_columns)
    cleaned_output["order_date"] = cleaned_output["order_date"].dt.strftime("%Y-%m-%d")
    cleaned_output["quantity"] = cleaned_output["quantity"].astype("int64")
    cleaned_output["sales_amount_zar"] = cleaned_output["sales_amount_zar"].round(2)

    exception_columns = ["source_row", *raw.columns, "issue_flags"]
    exceptions_output = exceptions[exception_columns].copy()

    issue_counts = Counter(
        flag.strip()
        for issue_text in data["issue_flags"]
        if issue_text
        for flag in issue_text.split(";")
    )
    summary = {
        "source_file": RAW_FILE.name,
        "raw_rows": int(len(data)),
        "accepted_rows": int(len(cleaned_output)),
        "exception_rows": int(len(exceptions_output)),
        "duplicate_id_rows": int(duplicate_id.sum()),
        "issue_counts": dict(sorted(issue_counts.items())),
        "accepted_sales_total_zar": round(float(cleaned_output["sales_amount_zar"].sum()), 2),
        "quality_rules": [
            "Transaction ID must be present and unique",
            "Order date must be parseable",
            "Customer must be present",
            "Region must map to a known region",
            "Quantity must be a positive number",
            "Amount must be a valid non-negative number",
        ],
    }
    return cleaned_output, exceptions_output, summary


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    raw = pd.read_csv(RAW_FILE, dtype="string", keep_default_na=False)
    cleaned, exceptions, summary = prepare_sales(raw)

    cleaned.to_csv(OUTPUT_DIR / "sales_cleaned.csv", index=False)
    exceptions.to_csv(OUTPUT_DIR / "sales_exceptions.csv", index=False)
    (OUTPUT_DIR / "quality_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
