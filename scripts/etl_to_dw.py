import pandas as pd
import sqlite3
import pathlib
import sys

# For local imports, temporarily add project root to sys.path
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Constants
DW_DIR = PROJECT_ROOT / "data" / "dw"
DW_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DW_DIR / "smart_sales.db"
PREPARED_DATA_DIR = PROJECT_ROOT / "data" / "prepared"

def create_schema(cursor: sqlite3.Cursor) -> None:
    """Drop and recreate tables in the data warehouse."""

    cursor.execute("DROP TABLE IF EXISTS sale")
    cursor.execute("DROP TABLE IF EXISTS product")
    cursor.execute("DROP TABLE IF EXISTS customer")

    cursor.execute("""
        CREATE TABLE customer (
            customer_id INTEGER PRIMARY KEY,
            name TEXT,
            region TEXT,
            join_date TEXT,
            last_active_year DATE,
            preferred_contact_method TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE product (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT,
            category TEXT,
            unit_price REAL,
            current_discount_percent REAL,
            subcategory TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE sale (
            sale_id INTEGER PRIMARY KEY,
            sale_date DATE, 
            customer_id INTEGER,
            product_id INTEGER,
            store_id INTEGER,
            campaign_id INTEGER,
            sale_amount REAL,
            bonus_points INTEGER,
            payment_type TEXT,
            FOREIGN KEY (customer_id) REFERENCES customer (customer_id),
            FOREIGN KEY (product_id) REFERENCES product (product_id)
        )
    """)

def delete_existing_records(cursor: sqlite3.Cursor) -> None:
    """Delete all existing records from the customer, product, and sale tables."""
    cursor.execute("DELETE FROM customer")
    cursor.execute("DELETE FROM product")
    cursor.execute("DELETE FROM sale")

def insert_customers(customers_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert customer data into the customer table."""
    customers_df.to_sql("customer", cursor.connection, if_exists="append", index=False)

def insert_products(products_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert product data into the product table."""
    products_df.to_sql("product", cursor.connection, if_exists="append", index=False)

def insert_sales(sales_df: pd.DataFrame, cursor: sqlite3.Cursor) -> None:
    """Insert sales data into the sales table."""
    sales_df.to_sql("sale", cursor.connection, if_exists="append", index=False)

def load_data_to_db() -> None:
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        create_schema(cursor)
        delete_existing_records(cursor)

        customers_df = pd.read_csv(PREPARED_DATA_DIR / "customers_data_prepared.csv")
        products_df = pd.read_csv(PREPARED_DATA_DIR / "products_data_prepared.csv")
        sales_df = pd.read_csv(PREPARED_DATA_DIR / "sales_data_prepared.csv")

        insert_customers(customers_df, cursor)
        insert_products(products_df, cursor)
        insert_sales(sales_df, cursor)

        conn.commit()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    load_data_to_db()
