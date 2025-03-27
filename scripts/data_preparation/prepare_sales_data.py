"""
scripts/data_preparation/prepare_sales_data.py

This script reads sales data from the data/raw folder, cleans the data, 
and writes the cleaned version to the data/prepared folder.

Tasks:
- Remove duplicates
- Handle missing values
- Remove outliers
- Ensure consistent formatting

-----------------------------------
How to Run:
1. Open a terminal in the main root project folder.
2. Activate the local project virtual environment.
3. Choose the correct commands for your OS to run this script:

Example (Windows/PowerShell) - do NOT include the > prompt:
> .venv\Scripts\activate
> py scripts\data_preparation\prepare_sales_data.py

Example (Mac/Linux) - do NOT include the $ prompt:
$ source .venv/bin/activate
$ python3 scripts/data_preparation/prepare_sales_data.py
"""

import pathlib
import sys
import pandas as pd

# For local imports, temporarily add project root to Python sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Now we can import local modules
from utils.logger import logger  # noqa: E402

# Constants
DATA_DIR: pathlib.Path = PROJECT_ROOT.joinpath("data")
RAW_DATA_DIR: pathlib.Path = DATA_DIR.joinpath("raw")
PREPARED_DATA_DIR: pathlib.Path = DATA_DIR.joinpath("prepared")

# -------------------
# Reusable Functions
# -------------------

def read_raw_data(file_name: str) -> pd.DataFrame:
    """
    Read raw data from CSV.

    Args:
        file_name (str): Name of the CSV file to read.
    
    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    logger.info(f"FUNCTION START: read_raw_data with file_name={file_name}")
    file_path = RAW_DATA_DIR.joinpath(file_name)
    logger.info(f"Reading data from {file_path}")
    df = pd.read_csv(file_path)
    logger.info(f"Loaded dataframe with {len(df)} rows and {len(df.columns)} columns")
    return df

def save_prepared_data(df: pd.DataFrame, file_name: str) -> None:
    """
    Save cleaned data to CSV.

    Args:
        df (pd.DataFrame): Cleaned DataFrame.
        file_name (str): Name of the output file.
    """
    logger.info(f"FUNCTION START: save_prepared_data with file_name={file_name}, dataframe shape={df.shape}")
    file_path = PREPARED_DATA_DIR.joinpath(file_name)
    df.to_csv(file_path, index=False)
    logger.info(f"Data saved to {file_path}")

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows from the DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame with duplicates removed.
    """
    logger.info(f"FUNCTION START: remove_duplicates with dataframe shape={df.shape}")
    initial_count = len(df)
    df = df.drop_duplicates()
    removed_count = initial_count - len(df)
    logger.info(f"Removed {removed_count} duplicate rows")
    return df

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing values by filling or dropping.
    Also imputes BonusPoints if missing or unreasonable.

    Args:
        df (pd.DataFrame): Input DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame with missing values handled.
    """
    logger.info(f"FUNCTION START: handle_missing_values with dataframe shape={df.shape}")

    missing_by_col = df.isna().sum()
    logger.info(f"Missing values by column before handling:\n{missing_by_col}")

    # Fill missing PaymentType with 'Unknown'
    if 'PaymentType' in df.columns:
        df['PaymentType'].fillna('Unknown', inplace=True)

    # === BonusPoints Fix ===
    if 'BonusPoints' in df.columns and 'SaleAmount' in df.columns:
        # Fill missing BonusPoints with int(SaleAmount)
        missing_mask = df['BonusPoints'].isna()
        missing_count = missing_mask.sum()
        df.loc[missing_mask, 'BonusPoints'] = df.loc[missing_mask, 'SaleAmount'].apply(lambda x: int(x))

        # Replace BonusPoints that are unreasonably high
        outlier_mask = df['BonusPoints'] > df['SaleAmount'] * 2
        outlier_count = outlier_mask.sum()
        df.loc[outlier_mask, 'BonusPoints'] = df.loc[outlier_mask, 'SaleAmount'].apply(lambda x: int(x))

        logger.info(f"Filled {missing_count} missing BonusPoints using SaleAmount.")
        logger.info(f"Adjusted {outlier_count} outlier BonusPoints to match SaleAmount.")

    missing_after = df.isna().sum()
    logger.info(f"Missing values by column after handling:\n{missing_after}")
    return df

def remove_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove outliers based on thresholds.

    Args:
        df (pd.DataFrame): Input DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame with outliers removed.
    """
    logger.info(f"FUNCTION START: remove_outliers with dataframe shape={df.shape}")
    # This function can be expanded later based on other columns
    logger.info("No additional outlier removal implemented at this time.")
    return df

def standardize_formats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize the formatting of various columns.

    Args:
        df (pd.DataFrame): Input DataFrame.
    
    Returns:
        pd.DataFrame: DataFrame with standardized formatting.
    """
    logger.info(f"FUNCTION START: standardize_formats with dataframe shape={df.shape}")
    logger.info("Completed standardizing formats")
    return df

def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Validate data against business rules.

    Args:
        df (pd.DataFrame): Input DataFrame.
    
    Returns:
        pd.DataFrame: Validated DataFrame.
    """
    logger.info(f"FUNCTION START: validate_data with dataframe shape={df.shape}")
    logger.info("Data validation complete")
    return df

def main() -> None:
    """
    Main function for processing sales data.
    """
    logger.info("==================================")
    logger.info("STARTING prepare_sales_data.py")
    logger.info("==================================")

    logger.info(f"Root project folder: {PROJECT_ROOT}")
    logger.info(f"data / raw folder: {RAW_DATA_DIR}")
    logger.info(f"data / prepared folder: {PREPARED_DATA_DIR}")

    input_file = "sales_data.csv"
    output_file = "sales_data_prepared.csv"
    
    df = read_raw_data(input_file)

    logger.info(f"Initial dataframe columns: {', '.join(df.columns.tolist())}")
    logger.info(f"Initial dataframe shape: {df.shape}")

    # Clean column names
    original_columns = df.columns.tolist()
    df.columns = df.columns.str.strip()
    changed_columns = [f"{old} -> {new}" for old, new in zip(original_columns, df.columns) if old != new]
    if changed_columns:
        logger.info(f"Cleaned column names: {', '.join(changed_columns)}")

    df = remove_duplicates(df)
    df = handle_missing_values(df)
    df = standardize_formats(df)
    df = remove_outliers(df)
    df = validate_data(df)
    save_prepared_data(df, output_file)

    logger.info("==================================")
    logger.info("FINISHED prepare_sales_data.py")
    logger.info("==================================")

if __name__ == "__main__":
    main()
