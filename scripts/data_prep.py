"""
Module 2: Initial Script to Verify Project Setup
File: scripts/data_prep.py
"""

import pathlib
import sys
import pandas as pd

# For local imports, temporarily add project root to Python sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Now we can import local modules
from utils.logger import logger

# Constants
DATA_DIR: pathlib.Path = PROJECT_ROOT.joinpath("data")
RAW_DATA_DIR: pathlib.Path = DATA_DIR.joinpath("raw")

def read_raw_data(file_name: str) -> pd.DataFrame:
    """Read raw data from CSV."""
    file_path: pathlib.Path = RAW_DATA_DIR.joinpath(file_name)
    try:
        logger.info(f"Reading raw data from {file_path}.")
        return pd.read_csv(file_path)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return pd.DataFrame()  # Return an empty DataFrame if the file is not found
    except Exception as e:
        logger.error(f"Error reading {file_path}: {e}")
        return pd.DataFrame()  # Return an empty DataFrame if any other error occurs

from scripts.data_scrubber import DataScrubber  # You wrote this!

def process_data(file_name: str) -> None:
    df = read_raw_data(file_name)
    if df.empty:
        return

    scrubber = DataScrubber = DataScrubber(df)
    scrubber.handle_missing_data(fill_value=0)
    scrubber.remove_duplicate_records()

    # Optional dataset-specific cleaning logic here:
    if "customers" in file_name:
        scrubber.format_column_strings_to_lower_and_trim("Name")
    elif "sales" in file_name:
        scrubber.parse_dates_to_add_standard_datetime("Date")

    # Save cleaned data
    cleaned_path = DATA_DIR.joinpath("clean", file_name.replace(".csv", "_clean.csv"))
    cleaned_path.parent.mkdir(parents=True, exist_ok=True)
    scrubber.df.to_csv(cleaned_path, index=False)


def main() -> None:
    """Main function for processing customer, product, and sales data."""
    logger.info("Starting data preparation...")
    process_data("customers_data.csv")
    process_data("products_data.csv")
    process_data("sales_data.csv")
    logger.info("Data preparation complete.")

if __name__ == "__main__":
    main()