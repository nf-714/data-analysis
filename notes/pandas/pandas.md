# Pandas — Zero to Hero

A complete reference for pandas, structured around the skills needed for a **Data Quality Control Associate** role.

---

## Table of Contents

1. [Setup & Imports](#1-setup--imports)
2. [Core Data Structures](#2-core-data-structures)
3. [Loading & Saving Data](#3-loading--saving-data)
4. [First Look at a Dataset](#4-first-look-at-a-dataset)
5. [Selecting & Filtering Data](#5-selecting--filtering-data)
6. [Data Quality Checks](#6-data-quality-checks)
7. [Cleaning Data](#7-cleaning-data)
8. [Working with Data Types](#8-working-with-data-types)
9. [String Operations](#9-string-operations)
10. [Dates & Times](#10-dates--times)
11. [Aggregation & Grouping](#11-aggregation--grouping)
12. [Merging & Joining](#12-merging--joining)
13. [Reshaping Data](#13-reshaping-data)
14. [Applying Functions](#14-applying-functions)
15. [Outlier Detection](#15-outlier-detection)
16. [Reporting & Exporting](#16-reporting--exporting)
17. [DQC Patterns Cheat Sheet](#17-dqc-patterns-cheat-sheet)

---

## 1. Setup & Imports

```python
pip install pandas numpy openpyxl ydata-profiling pandera
```

```python
import pandas as pd
import numpy as np

# Display settings — show all columns, wider output
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 100)
pd.set_option("display.width", 120)
pd.set_option("display.float_format", "{:.2f}".format)
```

---

## 2. Core Data Structures

### Series — a single column

```python
s = pd.Series([10, 20, 30, 40], name="scores")
s = pd.Series({"a": 1, "b": 2, "c": 3})   # dict → Series

s.index       # RangeIndex(start=0, stop=4, step=1)
s.values      # array([10, 20, 30, 40])
s.dtype       # dtype('int64')
s.name        # 'scores'
s[0]          # 10
s["a"]        # 1  (when using dict keys as index)
```

### DataFrame — a table (multiple columns)

```python
df = pd.DataFrame({
    "name":   ["Alice", "Bob", "Carol", "Dave"],
    "age":    [29, 34, 22, 45],
    "salary": [55000, 72000, 48000, 91000],
    "dept":   ["HR", "IT", "IT", "Finance"],
    "active": [True, True, False, True],
})

df.shape          # (4, 5)  → rows, columns
df.columns        # Index(['name', 'age', 'salary', 'dept', 'active'])
df.index          # RangeIndex(start=0, stop=4, step=1)
df.dtypes         # data type of each column
df.size           # total number of cells (rows × cols)
df.ndim           # 2
```

---

## 3. Loading & Saving Data

### Reading files

```python
# CSV
df = pd.read_csv("data.csv")
df = pd.read_csv("data.csv", sep=";")                     # different delimiter
df = pd.read_csv("data.csv", encoding="utf-8")
df = pd.read_csv("data.csv", parse_dates=["order_date"])  # auto-parse dates
df = pd.read_csv("data.csv", na_values=["N/A", "n/a", "-", ""])  # treat as NaN
df = pd.read_csv("data.csv", usecols=["id", "name", "email"])    # load specific cols
df = pd.read_csv("data.csv", nrows=1000)                  # first 1000 rows only
df = pd.read_csv("data.csv", skiprows=2)                  # skip header rows
df = pd.read_csv("data.csv", dtype={"zip_code": str})     # force column types

# Excel
df = pd.read_excel("data.xlsx", sheet_name="Sheet1")

# JSON
df = pd.read_json("data.json")

# SQL (requires sqlalchemy)
from sqlalchemy import create_engine
engine = create_engine("sqlite:///mydb.db")
df = pd.read_sql("SELECT * FROM customers", engine)
df = pd.read_sql_table("customers", engine)
```

### Saving files

```python
df.to_csv("output.csv", index=False)          # index=False avoids extra index column
df.to_excel("output.xlsx", index=False, sheet_name="Report")
df.to_json("output.json", orient="records")
df.to_sql("table_name", engine, if_exists="replace", index=False)
```

---

## 4. First Look at a Dataset

> Always run these 5 commands first on any new dataset.

```python
df.shape          # (rows, cols) — how big is this?
df.head(10)       # first 10 rows
df.tail(5)        # last 5 rows
df.info()         # column names, non-null counts, dtypes
df.describe()     # stats: count, mean, std, min, 25%, 50%, 75%, max
df.describe(include="all")     # includes object/categorical columns too
df.describe(include="object")  # only string columns
```

### Sample output from `df.info()` — what to look for:

```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 1000 entries, 0 to 999
Data columns (total 5 columns):
 #   Column      Non-Null Count  Dtype
---  ------      --------------  -----
 0   id          1000 non-null   int64       ← no nulls, good
 1   name        987 non-null    object      ← 13 nulls!
 2   email       950 non-null    object      ← 50 nulls!
 3   age         1000 non-null   float64     ← should be int? why float?
 4   created_at  1000 non-null   object      ← should be datetime!
```

---

## 5. Selecting & Filtering Data

### Selecting columns

```python
df["name"]                        # Series
df[["name", "age", "email"]]      # DataFrame (list of columns)
df.name                           # also works, but avoid — conflicts with methods
```

### Selecting rows

```python
df.loc[0]                         # row by label/index
df.loc[0:4]                       # rows 0 to 4 (inclusive)
df.loc[0:4, "name":"age"]         # rows 0–4, columns name to age
df.iloc[0]                        # row by integer position
df.iloc[0:4]                      # rows 0 to 3 (exclusive end)
df.iloc[0:4, 0:2]                 # rows 0–3, cols 0–1
df.iloc[-1]                       # last row
```

### Filtering rows (boolean indexing)

```python
df[df["age"] > 30]                              # age greater than 30
df[df["dept"] == "IT"]                          # exact match
df[df["dept"] != "IT"]                          # not equal
df[df["salary"].between(50000, 80000)]          # range check
df[df["name"].isin(["Alice", "Bob"])]           # in a list
df[~df["name"].isin(["Alice", "Bob"])]          # NOT in a list  (~ = not)

# Multiple conditions — use & (and), | (or), always wrap in ()
df[(df["age"] > 30) & (df["dept"] == "IT")]
df[(df["dept"] == "HR") | (df["dept"] == "Finance")]

# .query() — cleaner syntax for complex filters
df.query("age > 30 and dept == 'IT'")
df.query("salary > 50000 or dept == 'HR'")
df.query("age.between(25, 40)")                 # using pandas methods in query
```

### Sorting

```python
df.sort_values("salary")                        # ascending
df.sort_values("salary", ascending=False)       # descending
df.sort_values(["dept", "salary"])              # sort by multiple columns
df.sort_values("name", key=lambda x: x.str.lower())  # case-insensitive sort
```

---

## 6. Data Quality Checks

> This section is the heart of DQC work. Know every line.

### Completeness — missing values

```python
# Count nulls per column
df.isnull().sum()

# Percentage missing per column
(df.isnull().sum() / len(df) * 100).round(2)

# Rows where ANY column is null
df[df.isnull().any(axis=1)]

# Rows where a SPECIFIC column is null
df[df["email"].isnull()]

# Rows where ALL columns are null (completely empty rows)
df[df.isnull().all(axis=1)]

# Total null count across the entire dataframe
df.isnull().sum().sum()

# Heatmap of nulls (visual — requires seaborn)
import seaborn as sns
import matplotlib.pyplot as plt
sns.heatmap(df.isnull(), cbar=False, yticklabels=False)
plt.show()
```

### Uniqueness — duplicates

```python
# Count duplicate rows
df.duplicated().sum()

# Show all duplicate rows (both original and copy)
df[df.duplicated(keep=False)]

# Duplicates based on specific columns (e.g., same customer ID)
df.duplicated(subset=["customer_id"]).sum()
df[df.duplicated(subset=["customer_id"], keep=False)]

# Keep first occurrence, mark rest as duplicate
df[df.duplicated(subset=["customer_id"], keep="first")]

# Unique values in a column
df["dept"].unique()                   # array of unique values
df["dept"].nunique()                  # count of unique values
df["dept"].value_counts()             # frequency of each value
df["dept"].value_counts(normalize=True) * 100  # as percentage
```

### Validity — constraint checks

```python
# Numeric range check: flag rows where age is outside 0–120
invalid_age = df[~df["age"].between(0, 120)]

# Check for negative values in a column that should be positive
df[df["salary"] < 0]

# Check allowed categories
valid_statuses = ["active", "inactive", "pending"]
df[~df["status"].isin(valid_statuses)]

# Email format check using regex
invalid_emails = df[~df["email"].str.match(r".+@.+\..+", na=False)]

# Phone number format check
invalid_phones = df[~df["phone"].str.match(r"^\d{10}$", na=False)]

# Zip code length check
df[df["zip"].str.len() != 5]

# Date: flag future dates in a column that should be in the past
df[pd.to_datetime(df["birth_date"]) > pd.Timestamp.today()]
```

### Consistency — cross-column logic checks

```python
# Status says "active" but end_date is in the past
df[(df["status"] == "active") & (df["end_date"] < pd.Timestamp.today())]

# Hire date after termination date (impossible)
df[df["hire_date"] > df["termination_date"]]

# Revenue must equal quantity × price
df[df["revenue"] != df["quantity"] * df["unit_price"]]

# Parent-child relationship: child cannot exist without parent
orphaned = df[~df["department_id"].isin(departments_df["id"])]
```

### Accuracy — statistical anomaly checks

```python
# Summary stats to spot impossible or suspicious values
df["salary"].describe()

# Standard deviation-based outlier check (> 3 std from mean)
mean = df["salary"].mean()
std  = df["salary"].std()
df[(df["salary"] < mean - 3*std) | (df["salary"] > mean + 3*std)]

# Z-score approach
from scipy import stats
z_scores = np.abs(stats.zscore(df["salary"].dropna()))
df[z_scores > 3]
```

---

## 7. Cleaning Data

### Handling missing values

```python
# Drop rows where ANY column has a null
df.dropna()

# Drop rows where a SPECIFIC column is null
df.dropna(subset=["email"])

# Drop columns where more than 50% values are null
df.dropna(axis=1, thresh=int(0.5 * len(df)))

# Fill all nulls with a value
df.fillna(0)
df.fillna("Unknown")

# Fill specific columns
df["age"].fillna(df["age"].median(), inplace=True)
df["dept"].fillna("Unassigned", inplace=True)

# Forward fill (use previous row's value)
df["price"].ffill()

# Backward fill
df["price"].bfill()

# Fill with column mean/median/mode
df["salary"].fillna(df["salary"].mean(), inplace=True)
df["age"].fillna(df["age"].median(), inplace=True)
df["dept"].fillna(df["dept"].mode()[0], inplace=True)
```

### Removing duplicates

```python
# Remove exact duplicates, keep first occurrence
df.drop_duplicates()

# Remove duplicates based on key columns
df.drop_duplicates(subset=["customer_id"])
df.drop_duplicates(subset=["customer_id"], keep="last")

# Remove all duplicates (keep neither)
df.drop_duplicates(subset=["customer_id"], keep=False)
```

### Renaming columns

```python
df.rename(columns={"custmer_id": "customer_id", "Salary": "salary"})

# Lowercase all column names
df.columns = df.columns.str.lower()

# Replace spaces with underscores
df.columns = df.columns.str.replace(" ", "_")

# Strip whitespace from column names
df.columns = df.columns.str.strip()
```

### Dropping columns

```python
df.drop(columns=["unnecessary_col"])
df.drop(columns=["col1", "col2"])

# Drop columns with all nulls
df.dropna(axis=1, how="all")
```

### Resetting the index

```python
df.reset_index(drop=True)          # reset to 0,1,2,... and discard old index
df.set_index("customer_id")        # set a column as the index
```

---

## 8. Working with Data Types

### Checking and converting types

```python
df.dtypes                               # see all column types

# Convert types
df["age"] = df["age"].astype(int)
df["salary"] = df["salary"].astype(float)
df["customer_id"] = df["customer_id"].astype(str)
df["is_active"] = df["is_active"].astype(bool)

# Convert to categorical (saves memory, useful for columns with few unique values)
df["status"] = df["status"].astype("category")

# Convert to datetime
df["created_at"] = pd.to_datetime(df["created_at"])
df["created_at"] = pd.to_datetime(df["created_at"], format="%Y-%m-%d")
df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")  # bad → NaT

# Convert to numeric (non-numeric → NaN)
df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
```

### Memory optimization

```python
# Check memory usage
df.memory_usage(deep=True)
df.memory_usage(deep=True).sum() / 1024**2   # in MB

# Downcast numeric types
df["age"]    = pd.to_numeric(df["age"], downcast="integer")
df["price"]  = pd.to_numeric(df["price"], downcast="float")
df["status"] = df["status"].astype("category")
```

---

## 9. String Operations

> All string methods live under `.str` accessor. They are vectorized (fast on the whole column).

```python
# Case
df["name"].str.upper()
df["name"].str.lower()
df["name"].str.title()

# Whitespace
df["name"].str.strip()          # remove leading/trailing whitespace
df["name"].str.lstrip()
df["name"].str.rstrip()

# Check & search
df["email"].str.contains("@gmail")               # returns True/False Series
df["email"].str.startswith("admin")
df["email"].str.endswith(".org")
df["name"].str.match(r"^[A-Z][a-z]+$")           # regex match

# Extract
df["email"].str.split("@")                       # split into list
df["email"].str.split("@", expand=True)          # split into two columns
df["email"].str.extract(r"@(.+)")                # extract regex group

# Replace
df["phone"].str.replace("-", "", regex=False)    # remove dashes
df["name"].str.replace(r"\s+", " ", regex=True)  # normalize whitespace

# Length
df["zip"].str.len()

# Count occurrences
df["notes"].str.count("error")

# Practical DQC examples
df["email"].str.lower().str.strip()              # normalize emails
df[df["name"].str.contains(r"\d", na=False)]     # names containing numbers (suspicious)
df[df["phone"].str.len() != 10]                  # wrong phone length
```

---

## 10. Dates & Times

```python
# Parse dates
df["created_at"] = pd.to_datetime(df["created_at"])
df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")  # NaT on failure

# Extract components
df["year"]    = df["created_at"].dt.year
df["month"]   = df["created_at"].dt.month
df["day"]     = df["created_at"].dt.day
df["weekday"] = df["created_at"].dt.day_name()   # "Monday", "Tuesday"...
df["quarter"] = df["created_at"].dt.quarter

# Date arithmetic
df["days_since_signup"] = (pd.Timestamp.today() - df["created_at"]).dt.days
df["account_age_years"] = df["days_since_signup"] / 365

# Date range filters
df[df["created_at"] >= "2024-01-01"]
df[df["created_at"].between("2024-01-01", "2024-12-31")]

# Find records with invalid (future) dates
df[df["birth_date"] > pd.Timestamp.today()]

# Find records with missing or unparseable dates
df[df["created_at"].isnull()]    # NaT after coerce = bad date format

# Format dates for output
df["created_at"].dt.strftime("%Y-%m-%d")
df["created_at"].dt.strftime("%d/%m/%Y")
```

---

## 11. Aggregation & Grouping

```python
# Basic aggregations
df["salary"].sum()
df["salary"].mean()
df["salary"].median()
df["salary"].min()
df["salary"].max()
df["salary"].std()
df["salary"].var()
df["salary"].count()          # non-null count
df["salary"].nunique()        # unique count

# Aggregate multiple stats at once
df["salary"].agg(["min", "max", "mean", "std", "count"])

# GroupBy
df.groupby("dept")["salary"].mean()
df.groupby("dept")["salary"].agg(["min", "max", "mean", "count"])

# Multiple columns
df.groupby(["dept", "active"])["salary"].mean()

# Named aggregations (pandas 0.25+)
df.groupby("dept").agg(
    avg_salary=("salary", "mean"),
    max_salary=("salary", "max"),
    headcount=("name", "count"),
    null_emails=("email", lambda x: x.isnull().sum()),
)

# Useful for DQC: null count per group
df.groupby("dept")["email"].apply(lambda x: x.isnull().sum())

# Value counts across groups
df.groupby("dept")["status"].value_counts()
```

---

## 12. Merging & Joining

> Critical for consistency checks across tables.

```python
# Inner join — only matching rows from both
merged = pd.merge(orders, customers, on="customer_id", how="inner")

# Left join — all rows from left, NaN for non-matches on right
merged = pd.merge(orders, customers, on="customer_id", how="left")

# Right join
merged = pd.merge(orders, customers, on="customer_id", how="right")

# Outer join — all rows from both
merged = pd.merge(orders, customers, on="customer_id", how="outer")

# Join on columns with different names
pd.merge(orders, customers, left_on="cust_id", right_on="customer_id")

# Join on index
pd.merge(df1, df2, left_index=True, right_index=True)

# DQC use case: find orphaned records (orders with no matching customer)
merged = pd.merge(orders, customers, on="customer_id", how="left", indicator=True)
orphaned_orders = merged[merged["_merge"] == "left_only"]

# DQC use case: find customers with no orders
merged = pd.merge(customers, orders, on="customer_id", how="left", indicator=True)
no_orders = merged[merged["_merge"] == "left_only"]

# Concatenate DataFrames (stack vertically)
combined = pd.concat([df1, df2], ignore_index=True)

# Check for records in df1 not in df2 (set difference)
ids_only_in_df1 = set(df1["id"]) - set(df2["id"])
```

---

## 13. Reshaping Data

```python
# Pivot table
pivot = df.pivot_table(
    values="salary",
    index="dept",
    columns="active",
    aggfunc="mean",
    fill_value=0
)

# Melt — wide to long format (unpivot)
melted = df.melt(id_vars=["name"], value_vars=["q1_sales", "q2_sales", "q3_sales"],
                 var_name="quarter", value_name="sales")

# Stack / Unstack (for MultiIndex DataFrames)
df.stack()       # columns → rows
df.unstack()     # rows → columns

# Transpose
df.T
```

---

## 14. Applying Functions

```python
# Apply a function to a column (Series)
df["name"].apply(len)
df["salary"].apply(lambda x: x * 1.1)        # 10% raise

# Apply to entire DataFrame (row or column)
df.apply(lambda col: col.isnull().sum())      # null count per column
df.apply(lambda row: row["salary"] > 50000, axis=1)  # row-wise

# map — element-wise replacement (Series only)
status_map = {"active": 1, "inactive": 0, "pending": -1}
df["status_code"] = df["status"].map(status_map)

# applymap / map (DataFrame element-wise)
df[["col1", "col2"]].map(lambda x: str(x).strip())

# np.where — vectorized if/else
df["salary_band"] = np.where(df["salary"] > 70000, "High", "Low")

# pd.cut — bin continuous values into categories
df["age_group"] = pd.cut(df["age"], bins=[0, 18, 35, 60, 120],
                          labels=["Minor", "Young Adult", "Adult", "Senior"])

# pd.qcut — bin by quantile
df["salary_quartile"] = pd.qcut(df["salary"], q=4, labels=["Q1", "Q2", "Q3", "Q4"])
```

---

## 15. Outlier Detection

> A core DQC skill — know at least 3 methods.

### Method 1: IQR (Interquartile Range) — most common

```python
Q1  = df["salary"].quantile(0.25)
Q3  = df["salary"].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[(df["salary"] < lower_bound) | (df["salary"] > upper_bound)]
print(f"Found {len(outliers)} outliers")
```

### Method 2: Z-Score — good for normally distributed data

```python
mean = df["salary"].mean()
std  = df["salary"].std()

df["z_score"] = (df["salary"] - mean) / std
outliers = df[df["z_score"].abs() > 3]
```

### Method 3: Percentile clipping

```python
lower = df["salary"].quantile(0.01)   # bottom 1%
upper = df["salary"].quantile(0.99)   # top 1%

outliers = df[(df["salary"] < lower) | (df["salary"] > upper)]

# Clip outliers instead of removing
df["salary_clipped"] = df["salary"].clip(lower, upper)
```

### Applying to multiple numeric columns

```python
numeric_cols = df.select_dtypes(include=np.number).columns

for col in numeric_cols:
    Q1  = df[col].quantile(0.25)
    Q3  = df[col].quantile(0.75)
    IQR = Q3 - Q1
    mask = (df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)
    print(f"{col}: {mask.sum()} outliers")
```

---

## 16. Reporting & Exporting

### Quick text summary

```python
def quality_report(df: pd.DataFrame) -> None:
    print("=" * 50)
    print(f"Shape: {df.shape}")
    print(f"\nMissing values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
    print(f"\nDuplicate rows: {df.duplicated().sum()}")
    print(f"\nData types:\n{df.dtypes}")
    print(f"\nNumeric summary:\n{df.describe()}")
    print("=" * 50)

quality_report(df)
```

### Automated HTML report with ydata-profiling

```python
from ydata_profiling import ProfileReport

profile = ProfileReport(df, title="Data Quality Report", explorative=True)
profile.to_file("dq_report.html")      # open in browser
profile.to_notebook_iframe()           # if using Jupyter
```

### Styled Excel export with issues highlighted

```python
writer = pd.ExcelWriter("dq_report.xlsx", engine="openpyxl")

df.to_excel(writer, sheet_name="Raw Data", index=False)

# Write issues sheet
issues = pd.DataFrame({
    "Column": ["email", "age", "customer_id"],
    "Issue":  ["50 nulls (5%)", "12 outliers", "3 duplicates"],
    "Severity": ["Medium", "Low", "High"],
})
issues.to_excel(writer, sheet_name="Quality Issues", index=False)

writer.close()
```

---

## 17. DQC Patterns Cheat Sheet

> Copy these into any new data audit project.

```python
import pandas as pd
import numpy as np

# ── LOAD ─────────────────────────────────────────────────────────────────────
df = pd.read_csv("data.csv", parse_dates=["created_at"], dtype={"zip": str})

# ── PROFILE ──────────────────────────────────────────────────────────────────
print(df.shape)
print(df.info())
print(df.describe(include="all"))

# ── COMPLETENESS ─────────────────────────────────────────────────────────────
null_pct = (df.isnull().sum() / len(df) * 100).round(2)
print(null_pct[null_pct > 0])

# ── UNIQUENESS ───────────────────────────────────────────────────────────────
print(df.duplicated().sum())
print(df.duplicated(subset=["id"]).sum())

# ── VALIDITY ─────────────────────────────────────────────────────────────────
print(df[~df["age"].between(0, 120)])
print(df[~df["email"].str.match(r".+@.+\..+", na=False)])
print(df[~df["status"].isin(["active", "inactive", "pending"])])

# ── CONSISTENCY ──────────────────────────────────────────────────────────────
print(df[(df["status"] == "active") & (df["end_date"] < pd.Timestamp.today())])
print(df[df["hire_date"] > df["termination_date"]])

# ── OUTLIERS (IQR) ────────────────────────────────────────────────────────────
for col in df.select_dtypes(include=np.number).columns:
    Q1, Q3 = df[col].quantile([0.25, 0.75])
    IQR = Q3 - Q1
    n = ((df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)).sum()
    if n: print(f"  {col}: {n} outliers")

# ── CLEAN ────────────────────────────────────────────────────────────────────
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df.drop_duplicates(subset=["id"], inplace=True)
df.dropna(subset=["id", "email"], inplace=True)
df["age"].fillna(df["age"].median(), inplace=True)
df["email"] = df["email"].str.lower().str.strip()

# ── EXPORT ───────────────────────────────────────────────────────────────────
df.to_csv("cleaned_data.csv", index=False)
```

---

## Quick Reference — Most Used Methods

| Task | Method |
|---|---|
| Load CSV | `pd.read_csv("file.csv")` |
| Shape | `df.shape` |
| Column types | `df.dtypes` |
| Summary stats | `df.describe()` |
| Null counts | `df.isnull().sum()` |
| Null percentage | `df.isnull().mean() * 100` |
| Duplicate count | `df.duplicated().sum()` |
| Show duplicates | `df[df.duplicated(keep=False)]` |
| Filter rows | `df[df["col"] > value]` |
| Multiple filters | `df[(cond1) & (cond2)]` |
| Unique values | `df["col"].unique()` |
| Value frequency | `df["col"].value_counts()` |
| Fill nulls | `df["col"].fillna(value)` |
| Drop null rows | `df.dropna(subset=["col"])` |
| Drop duplicates | `df.drop_duplicates(subset=["col"])` |
| Rename columns | `df.rename(columns={"old": "new"})` |
| Lowercase cols | `df.columns.str.lower()` |
| Convert type | `df["col"].astype(int)` |
| Parse dates | `pd.to_datetime(df["col"])` |
| String contains | `df["col"].str.contains("x")` |
| Group + aggregate | `df.groupby("col").agg(...)` |
| Merge tables | `pd.merge(df1, df2, on="id")` |
| Sort | `df.sort_values("col", ascending=False)` |
| Apply function | `df["col"].apply(func)` |
| IQR outliers | `Q1, Q3 = df.quantile([.25, .75])` |
| Export CSV | `df.to_csv("out.csv", index=False)` |

---

*Last updated: April 2026 | Role focus: Data Quality Control Associate*
