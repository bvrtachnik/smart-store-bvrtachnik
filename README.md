# Project Setup

## Project Initialization

### Create a GitHub Repository
- Create a new repo on GitHub and add a default README.

### Clone the Repository
```shell
git clone [your-repo-url]
cd [cloned-repo]
```

### Add `.gitignore` and `requirements.txt` Files
- Add `.gitignore` and `requirements.txt` to the project.

### Create and Activate a Virtual Environment
```shell
python -m venv .venv
.\.venv\Scripts\Activate
```

### Upgrade Pip, Setuptools, and Wheel
```shell
py -m pip install --upgrade pip setuptools wheel
```

### Install Dependencies
```shell
pip install -r requirements.txt
```

### Track and Push Changes with Git
```shell
git add .
git commit -m "Initial commit"
git push origin main
```

## Data Cleaning Process

### Data Cleaning Scripts

Scripts were developed to clean data and perform the following operations:

- **Remove Duplicates**: Eliminate any duplicate records.
- **Handle Missing Values**: Address missing data through imputation.
- **Standardize Formatting**: Apply consistent casing and whitespace trimming.
- **Parse Dates**: Convert date fields into a standardized datetime format.

To execute a script within the `scripts` folder:

```shell
py scripts\data_prep.py
```

## Data Warehouse Creation

### Overview

The cleaned data is loaded into a SQLite data warehouse (`smart_sales.db`) located in the `data/dw` directory. The warehouse includes three main tables:

- `customer`
- `product`
- `sale`

These tables are recreated each time the ETL script is run to ensure consistency.

### Running the ETL Script

To create the database, tables, and insert data from the cleaned CSV files:

```shell
py scripts\etl_to_dw.py
```
## Database Schema

### `customer` Table

| Column Name              | Data Type | Description                          |
|--------------------------|-----------|--------------------------------------|
| customer_id              | INTEGER   | Primary key                          |
| name                     | TEXT      | Customer's full name                 |
| region                   | TEXT      | Region where customer resides        |
| join_date                | TEXT      | Date the customer joined             |
| last_active_year         | DATE      | Last year the customer was active    |
| preferred_contact_method | TEXT      | Preferred communication method       |

---

### `product` Table

| Column Name              | Data Type | Description                                |
|--------------------------|-----------|--------------------------------------------|
| product_id               | INTEGER   | Primary key                                |
| product_name             | TEXT      | Name of the product                        |
| category                 | TEXT      | Main product category                      |
| unit_price               | REAL      | Price per unit                             |
| current_discount_percent | REAL      | Current discount percentage on the product |
| subcategory              | TEXT      | Subcategory under the main category        |

---

### `sale` Table

| Column Name   | Data Type | Description                                |
|---------------|-----------|--------------------------------------------|
| sale_id       | INTEGER   | Primary key                                |
| sale_date     | DATE      | Date the sale occurred                     |
| customer_id   | INTEGER   | Foreign key referencing `customer` table   |
| product_id    | INTEGER   | Foreign key referencing `product` table    |
| store_id      | INTEGER   | ID of the store where sale happened        |
| campaign_id   | INTEGER   | ID of the marketing campaign               |
| sale_amount   | REAL      | Total amount of the sale                   |
| bonus_points  | INTEGER   | Points earned from the purchase            |
| payment_type  | TEXT      | Payment method used                        |


## Table Previews

### Customer Table
![Customer Table](../customer_table_screenshot.png)

### Product Table
![Product Table](../product_table_screenshot.png)

### Sale Table
![Sale Table](../sale_table_screenshot.png)

## Notes

- This project uses `pandas` for data manipulation and `sqlite3` for database interactions.
- The ETL process is repeatable and can be run multiple times without manual cleanup.
- The resulting SQLite database can be queried directly or connected to BI tools for further analysis.
