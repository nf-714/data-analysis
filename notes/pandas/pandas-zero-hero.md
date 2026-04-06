# Pandas Zero to Hero — Lessons

Hands-on lessons that take you from knowing Python to writing production-grade data quality code.
Each lesson builds on the previous one. Do them in order.

---

## Lesson 1 — Your First DataFrame

**Goal:** Understand what a DataFrame is and how to create one from scratch.

```python
import pandas as pd

# A DataFrame is just a table — rows and columns
df = pd.DataFrame({
    "employee_id": [101, 102, 103, 104],
    "name":        ["Alice", "Bob", "Carol", "Dave"],
    "department":  ["HR", "IT", "IT", "Finance"],
    "salary":      [55000, 72000, 48000, 91000],
    "active":      [True, True, False, True],
})

print(df)
```

**Output:**
```
   employee_id   name department  salary  active
0          101  Alice         HR   55000    True
1          102    Bob         IT   72000    True
2          103  Carol         IT   48000   False
3          104   Dave    Finance   91000    True
```

**Practice tasks:**
1. Print only the `name` column: `df["name"]`
2. Print only rows where `active` is `True`: `df[df["active"] == True]`
3. Print `df.shape` — what does it return and what does it mean?
4. Print `df.dtypes` — what type did pandas assign to each column?
5. Add a new column `"bonus"` where every employee gets 10% of their salary

---

## Lesson 2 — Loading Real Data

**Goal:** Load a CSV file and understand the shape of the data before touching it.

```python
import pandas as pd

df = pd.read_csv("dataset/banklist.csv")

# The 5 commands you run EVERY time you open a new dataset
print(df.shape)           # (rows, columns)
print(df.columns.tolist()) # column names
print(df.dtypes)          # data types
print(df.head(5))         # first 5 rows
print(df.info())          # full overview — nulls, types, memory
```

**The questions you should always ask:**
- How many rows and columns are there?
- What does each column represent?
- Are any columns parsed as the wrong type? (dates as strings, numbers as objects)
- Are there any obvious nulls at first glance?

```python
# Full statistical summary
print(df.describe())               # numeric columns
print(df.describe(include="all"))  # ALL columns including strings
```

**Practice tasks:**
1. What is the shape of the banklist dataset?
2. Which columns have null values? (use `df.isnull().sum()`)
3. What data type is the `"Closing Date"` column? What should it be?
4. How many unique states appear in the dataset? (`df["ST"].nunique()`)
5. Which state has the most bank failures? (`df["ST"].value_counts().head(5)`)

---

## Lesson 3 — Selecting & Filtering

**Goal:** Retrieve exactly the rows and columns you need.

```python
import pandas as pd

df = pd.read_csv("dataset/banklist.csv")

# --- Selecting columns ---
df["Bank Name"]                          # single column → Series
df[["Bank Name", "ST", "CERT"]]         # multiple columns → DataFrame

# --- Selecting rows by position ---
df.iloc[0]          # first row
df.iloc[-1]         # last row
df.iloc[0:5]        # rows 0–4
df.iloc[0:5, 0:3]   # rows 0–4, columns 0–2

# --- Selecting rows by label ---
df.loc[0]           # row with index label 0
df.loc[0:4]         # rows 0 to 4 (INCLUSIVE, unlike iloc)

# --- Filtering by condition ---
df[df["ST"] == "GA"]                         # Georgia only
df[df["ST"] != "CA"]                         # everything except California
df[df["CERT"] > 20000]                       # cert number > 20000

# --- Multiple conditions ---
df[(df["ST"] == "GA") & (df["CERT"] > 10000)]    # AND
df[(df["ST"] == "GA") | (df["ST"] == "FL")]       # OR

# --- .query() — cleaner for complex filters ---
df.query("ST == 'GA' and CERT > 10000")
df.query("ST in ['GA', 'FL', 'TX']")
```

**Practice tasks:**
1. Select only banks in Texas (`"TX"`)
2. Select all columns except `"CERT"` (use `df.drop(columns=["CERT"])`)
3. Find all banks acquired by `"No Acquirer"` — how many are there?
4. Find all banks in California OR Florida — sort them by `"Bank Name"`
5. Use `.query()` to find banks in New York with CERT < 5000

---

## Lesson 4 — Spotting Data Quality Problems (The DQC Mindset)

**Goal:** Audit a dataset systematically using the 6 quality dimensions.

```python
import pandas as pd

df = pd.read_csv("dataset/banklist.csv")

# ── DIMENSION 1: COMPLETENESS ────────────────────────────────────────────────
# Are all fields filled in? Are there missing values?

print(df.isnull().sum())                              # count nulls per column
print((df.isnull().sum() / len(df) * 100).round(2))  # % missing per column
print(df[df.isnull().any(axis=1)])                    # rows with ANY null

# ── DIMENSION 2: UNIQUENESS ──────────────────────────────────────────────────
# Are there unintended duplicate rows?

print(df.duplicated().sum())                                    # total duplicates
print(df.duplicated(subset=["CERT"]).sum())                     # duplicate on key column
print(df[df.duplicated(subset=["CERT"], keep=False)])           # show them

# ── DIMENSION 3: VALIDITY ────────────────────────────────────────────────────
# Does data follow expected formats and rules?

# CERT should be a positive number
print(df[df["CERT"] <= 0])

# State should be a 2-letter code
print(df[df["ST"].str.len() != 2])

# Check for unexpected categories
print(df["ST"].value_counts())    # visually check for weird values

# ── DIMENSION 4: CONSISTENCY ──────────────────────────────────────────────────
# Does data contradict itself?

df["Closing Date"] = pd.to_datetime(df["Closing Date"], errors="coerce")
df["Updated Date"] = pd.to_datetime(df["Updated Date"], errors="coerce")

# A closing date should never be after the updated date
print(df[df["Closing Date"] > df["Updated Date"]])

# ── DIMENSION 5: ACCURACY ────────────────────────────────────────────────────
# Are numeric values statistically plausible?

print(df["CERT"].describe())
print(df[df["CERT"] < 0])         # negative cert numbers = impossible

# ── DIMENSION 6: TIMELINESS ──────────────────────────────────────────────────
# Is there data from the future? Dates that seem stale?

today = pd.Timestamp.today()
print(df[df["Closing Date"] > today])   # closing date in the future?
```

**Practice tasks:**
1. Which columns have missing values in the banklist? How many?
2. Are there any duplicate CERT numbers?
3. Are all state codes exactly 2 characters?
4. Are there any closing dates that are in the future?
5. Write a function `audit(df)` that runs all 5 checks and prints a summary

---

## Lesson 5 — Cleaning Data

**Goal:** Fix the problems you found in Lesson 4.

```python
import pandas as pd

df = pd.read_csv("dataset/banklist.csv")

# ── Step 1: Standardize column names ─────────────────────────────────────────
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
print(df.columns.tolist())

# ── Step 2: Fix data types ────────────────────────────────────────────────────
df["closing_date"] = pd.to_datetime(df["closing_date"], errors="coerce")
df["updated_date"] = pd.to_datetime(df["updated_date"], errors="coerce")
# errors="coerce" → bad dates become NaT instead of crashing

# ── Step 3: Handle missing values ─────────────────────────────────────────────
print(df.isnull().sum())

# Option A: Drop rows where a critical column is null
df_clean = df.dropna(subset=["cert"])

# Option B: Fill nulls with a meaningful default
df["acquiring_institution"].fillna("No Acquirer", inplace=True)

# Option C: Fill numeric nulls with the median
# df["some_number"].fillna(df["some_number"].median(), inplace=True)

# ── Step 4: Remove duplicates ──────────────────────────────────────────────────
before = len(df)
df.drop_duplicates(subset=["cert"], inplace=True)
after = len(df)
print(f"Removed {before - after} duplicate rows")

# ── Step 5: Clean string columns ──────────────────────────────────────────────
df["bank_name"]             = df["bank_name"].str.strip()
df["st"]                    = df["st"].str.upper().str.strip()
df["acquiring_institution"] = df["acquiring_institution"].str.strip()

# ── Step 6: Validate the result ────────────────────────────────────────────────
print(df.isnull().sum())          # should be lower now
print(df.duplicated().sum())      # should be 0
print(df.dtypes)                  # dates should now be datetime64
print(df.shape)                   # check row count didn't change unexpectedly
```

**Practice tasks:**
1. Run the full cleaning script on the banklist
2. After cleaning, how many rows remain?
3. How many banks closed each year? (`df["closing_date"].dt.year.value_counts()`)
4. Which year had the most bank failures?
5. Export the cleaned data to `dataset/banklist_clean.csv`

---

## Lesson 6 — Aggregation & Grouping

**Goal:** Summarize data to find patterns and answer business questions.

```python
import pandas as pd

df = pd.read_csv("dataset/banklist.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df["closing_date"] = pd.to_datetime(df["closing_date"], errors="coerce")
df["year"] = df["closing_date"].dt.year

# --- Basic aggregation ---
print(len(df))                       # total banks
print(df["st"].nunique())            # how many unique states

# --- GroupBy ---
# How many banks failed per state?
by_state = df.groupby("st")["bank_name"].count().sort_values(ascending=False)
print(by_state.head(10))

# --- Multiple aggregations ---
summary = df.groupby("st").agg(
    bank_count    = ("bank_name", "count"),
    earliest_fail = ("closing_date", "min"),
    latest_fail   = ("closing_date", "max"),
)
print(summary.head(10))

# --- Group by year ---
by_year = df.groupby("year")["bank_name"].count()
print(by_year)

# --- Pivot table ---
pivot = df.pivot_table(
    values="bank_name",
    index="year",
    columns="st",
    aggfunc="count",
    fill_value=0
)
print(pivot.head())
```

**Practice tasks:**
1. Which 5 states had the most bank failures?
2. In which year did the most banks fail?
3. Which acquiring institution took over the most failed banks?
4. Build a year-over-year summary: year, count of failures
5. Which state had bank failures spanning the widest date range?

---

## Lesson 7 — String Operations for Data Validation

**Goal:** Use the `.str` accessor to validate and clean text data.

```python
import pandas as pd

df = pd.DataFrame({
    "name":  ["  Alice Johnson ", "bob SMITH", "CAROL  ", "dave o'brien", "Eve123"],
    "email": ["alice@example.com", "BOB@GMAIL.COM", "carol@", "dave@company.co.uk", None],
    "phone": ["555-123-4567", "5551234567", "555.123.4567", "123", "555-123-456700"],
    "zip":   ["12345", "9021", "123456", "10001", "90210"],
})

# ── Normalize strings ─────────────────────────────────────────────────────────
df["name"]  = df["name"].str.strip().str.title()
df["email"] = df["email"].str.lower().str.strip()

# ── Validate email format ──────────────────────────────────────────────────────
valid_email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
df["email_valid"] = df["email"].str.match(valid_email_pattern, na=False)
print(df[~df["email_valid"]])

# ── Validate phone format (10 digits after stripping non-numeric) ──────────────
df["phone_digits"] = df["phone"].str.replace(r"\D", "", regex=True)  # keep only digits
df["phone_valid"]  = df["phone_digits"].str.len() == 10
print(df[~df["phone_valid"]])

# ── Validate zip code (exactly 5 digits) ──────────────────────────────────────
df["zip_valid"] = df["zip"].str.match(r"^\d{5}$", na=False)
print(df[~df["zip_valid"]])

# ── Find suspicious names (containing digits) ─────────────────────────────────
print(df[df["name"].str.contains(r"\d", na=False)])

# ── Summary: how many invalid per field? ─────────────────────────────────────
print(f"Invalid emails: {(~df['email_valid']).sum()}")
print(f"Invalid phones: {(~df['phone_valid']).sum()}")
print(f"Invalid zips:   {(~df['zip_valid']).sum()}")
```

**Practice tasks:**
1. Create a DataFrame of 10 made-up customer records — include intentional errors
2. Write a validation check for each column
3. Flag every row that has at least one invalid field
4. Export only the invalid rows to `invalid_records.csv`
5. What percentage of records are fully valid?

---

## Lesson 8 — Dates & Time-Based Quality Checks

**Goal:** Parse, validate, and analyze date columns.

```python
import pandas as pd

df = pd.DataFrame({
    "order_id":   [1, 2, 3, 4, 5, 6],
    "order_date": ["2024-01-15", "2024-02-30", "not-a-date", "2026-12-01", "2023-11-05", None],
    "ship_date":  ["2024-01-18", "2024-02-28", "2024-03-10", "2026-11-30", "2023-11-01", "2024-06-01"],
})

today = pd.Timestamp.today()

# ── Parse dates, coerce bad values to NaT ─────────────────────────────────────
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
df["ship_date"]  = pd.to_datetime(df["ship_date"],  errors="coerce")

# ── Check 1: Unparseable dates (NaT after coerce) ─────────────────────────────
print("Unparseable order dates:")
print(df[df["order_date"].isnull()])

# ── Check 2: Future dates (order date is in the future) ───────────────────────
print("\nFuture order dates:")
print(df[df["order_date"] > today])

# ── Check 3: Logical inconsistency (ship before order) ────────────────────────
print("\nShipped before ordered:")
print(df[df["ship_date"] < df["order_date"]])

# ── Check 4: Extract components for analysis ──────────────────────────────────
df["order_year"]  = df["order_date"].dt.year
df["order_month"] = df["order_date"].dt.month
df["order_day"]   = df["order_date"].dt.day_name()

# ── Check 5: Calculate time differences ───────────────────────────────────────
df["days_to_ship"] = (df["ship_date"] - df["order_date"]).dt.days
print("\nDays to ship:")
print(df[["order_id", "order_date", "ship_date", "days_to_ship"]])

# ── Check 6: Flag abnormally long ship times ───────────────────────────────────
print("\nOrders taking > 7 days to ship:")
print(df[df["days_to_ship"] > 7])
```

**Practice tasks:**
1. Apply date parsing to the banklist `"Closing Date"` and `"Updated Date"` columns
2. Find any rows where `"Updated Date"` is before `"Closing Date"` (illogical)
3. How many banks failed per month? (use `.dt.month`)
4. What was the longest gap between a closing date and its updated date?
5. Flag any banks where `"Updated Date"` is in the future

---

## Lesson 9 — Outlier Detection

**Goal:** Find records with statistically abnormal numeric values.

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "employee_id": range(1, 21),
    "salary": [
        52000, 58000, 61000, 47000, 55000,
        63000, 59000, 54000, 67000, 51000,
        60000, 56000, 500000,   # ← outlier: probably a data entry error
        49000, 62000, 57000, 53000, 48000,
        -5000,   # ← outlier: negative salary is impossible
        65000,
    ],
    "age": [
        28, 34, 42, 25, 31, 39, 27, 45, 33, 29,
        36, 41, 999, 24, 38, 32, 44, 26, 30, 37  # ← 999 is invalid
    ]
})

# ── METHOD 1: IQR (Interquartile Range) ───────────────────────────────────────
def find_outliers_iqr(series):
    Q1  = series.quantile(0.25)
    Q3  = series.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    return series[(series < lower) | (series > upper)]

salary_outliers = find_outliers_iqr(df["salary"])
age_outliers    = find_outliers_iqr(df["age"])

print("Salary outliers (IQR):")
print(df.loc[salary_outliers.index, ["employee_id", "salary"]])

print("\nAge outliers (IQR):")
print(df.loc[age_outliers.index, ["employee_id", "age"]])

# ── METHOD 2: Z-Score ─────────────────────────────────────────────────────────
def find_outliers_zscore(series, threshold=3):
    mean = series.mean()
    std  = series.std()
    z    = (series - mean) / std
    return series[z.abs() > threshold]

print("\nSalary outliers (Z-score):")
print(find_outliers_zscore(df["salary"]))

# ── METHOD 3: Run on ALL numeric columns ─────────────────────────────────────
numeric_cols = df.select_dtypes(include=np.number).columns.drop("employee_id")

print("\n── Outlier Summary ──")
for col in numeric_cols:
    Q1, Q3 = df[col].quantile([0.25, 0.75])
    IQR    = Q3 - Q1
    mask   = (df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)
    print(f"  {col}: {mask.sum()} outlier(s) → {df.loc[mask, col].tolist()}")
```

**Practice tasks:**
1. Apply IQR outlier detection to the banklist `"CERT"` column
2. Which method (IQR vs Z-score) catches more outliers on the salary column? Why?
3. Build a function `outlier_report(df)` that runs IQR on all numeric columns and returns a DataFrame of findings
4. After identifying outliers, should you remove them or flag them? Write 2 sentences explaining when to do each
5. Clip the salary column so no value is below the 1st percentile or above the 99th

---

## Lesson 10 — Building a Full DQC Audit Script

**Goal:** Tie everything together into a reusable, professional audit tool.

```python
import pandas as pd
import numpy as np
from dataclasses import dataclass, field
from typing import List

# ── Data structure for an individual issue ────────────────────────────────────
@dataclass
class QualityIssue:
    dimension:     str    # Completeness / Uniqueness / Validity / Consistency / Accuracy
    column:        str
    description:   str
    affected_rows: int
    severity:      str    # High / Medium / Low

# ── Individual check functions ────────────────────────────────────────────────
def check_completeness(df: pd.DataFrame) -> List[QualityIssue]:
    issues = []
    for col in df.columns:
        n = df[col].isnull().sum()
        if n == 0:
            continue
        pct = n / len(df) * 100
        severity = "High" if pct > 20 else "Medium" if pct > 5 else "Low"
        issues.append(QualityIssue(
            dimension="Completeness",
            column=col,
            description=f"{n} null values ({pct:.1f}%)",
            affected_rows=n,
            severity=severity,
        ))
    return issues


def check_uniqueness(df: pd.DataFrame, key_cols: list) -> List[QualityIssue]:
    issues = []
    n = df.duplicated(subset=key_cols).sum()
    if n > 0:
        issues.append(QualityIssue(
            dimension="Uniqueness",
            column=str(key_cols),
            description=f"{n} duplicate rows based on {key_cols}",
            affected_rows=n,
            severity="High",
        ))
    return issues


def check_future_dates(df: pd.DataFrame, date_cols: list) -> List[QualityIssue]:
    issues = []
    today = pd.Timestamp.today()
    for col in date_cols:
        if col not in df.columns:
            continue
        parsed = pd.to_datetime(df[col], errors="coerce")
        n = (parsed > today).sum()
        if n > 0:
            issues.append(QualityIssue(
                dimension="Validity",
                column=col,
                description=f"{n} future dates found",
                affected_rows=n,
                severity="Medium",
            ))
    return issues


def check_outliers(df: pd.DataFrame, numeric_cols: list = None) -> List[QualityIssue]:
    issues = []
    cols = numeric_cols or df.select_dtypes(include=np.number).columns.tolist()
    for col in cols:
        series = df[col].dropna()
        Q1, Q3 = series.quantile([0.25, 0.75])
        IQR    = Q3 - Q1
        mask   = (df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)
        n      = mask.sum()
        if n > 0:
            issues.append(QualityIssue(
                dimension="Accuracy",
                column=col,
                description=f"{n} outlier(s) outside IQR bounds [{Q1 - 1.5*IQR:.2f}, {Q3 + 1.5*IQR:.2f}]",
                affected_rows=n,
                severity="Low" if n < 5 else "Medium",
            ))
    return issues


# ── Main audit runner ──────────────────────────────────────────────────────────
def run_audit(
    df:         pd.DataFrame,
    key_cols:   list = None,
    date_cols:  list = None,
    label:      str  = "Dataset",
) -> pd.DataFrame:

    all_issues: List[QualityIssue] = []
    all_issues += check_completeness(df)
    all_issues += check_uniqueness(df, key_cols or [df.columns[0]])
    all_issues += check_future_dates(df, date_cols or [])
    all_issues += check_outliers(df)

    if not all_issues:
        print(f"✓ {label}: No issues found.")
        return pd.DataFrame()

    report = pd.DataFrame([vars(i) for i in all_issues])
    report = report.sort_values(
        "severity",
        key=lambda s: s.map({"High": 0, "Medium": 1, "Low": 2})
    )

    print(f"\n{'='*60}")
    print(f"  DQC AUDIT REPORT — {label}")
    print(f"  Rows: {len(df):,}  |  Columns: {len(df.columns)}  |  Issues: {len(all_issues)}")
    print(f"{'='*60}")
    print(report.to_string(index=False))
    print(f"{'='*60}\n")

    return report


# ── Run it ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    df = pd.read_csv("dataset/banklist.csv")
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    report = run_audit(
        df,
        key_cols=["cert"],
        date_cols=["closing_date", "updated_date"],
        label="Bank Failure List",
    )

    report.to_csv("dqc_audit_report.csv", index=False)
    print("Report saved to dqc_audit_report.csv")
```

**Practice tasks:**
1. Run the audit script on the banklist dataset — what issues does it find?
2. Add a `check_string_whitespace(df)` function that flags columns where any value has leading/trailing spaces
3. Add a `check_negative_values(df, cols)` function for columns that should never be negative
4. Modify `run_audit()` to also print a 1-line summary: `"X High, Y Medium, Z Low severity issues"`
5. Export both the cleaned data AND the audit report as separate sheets in one Excel file

---

## Lesson 11 — Merging Tables & Cross-Table Validation

**Goal:** Validate data integrity across multiple related tables.

```python
import pandas as pd

# Two related tables
customers = pd.DataFrame({
    "customer_id": [1, 2, 3, 4, 5],
    "name":        ["Alice", "Bob", "Carol", "Dave", "Eve"],
    "email":       ["a@x.com", "b@x.com", "c@x.com", "d@x.com", "e@x.com"],
})

orders = pd.DataFrame({
    "order_id":    [101, 102, 103, 104, 105, 106],
    "customer_id": [1, 2, 3, 6, 2, 99],  # 6 and 99 don't exist in customers!
    "amount":      [250, 180, 320, 90, 150, 400],
    "status":      ["shipped", "pending", "shipped", "pending", "cancelled", "shipped"],
})

# ── Check 1: Referential integrity ────────────────────────────────────────────
# Orders that reference a non-existent customer (orphaned records)
merged = pd.merge(orders, customers, on="customer_id", how="left", indicator=True)
orphaned = merged[merged["_merge"] == "left_only"]
print(f"Orphaned orders: {len(orphaned)}")
print(orphaned[["order_id", "customer_id", "amount"]])

# ── Check 2: Customers with no orders ──────────────────────────────────────────
merged2 = pd.merge(customers, orders, on="customer_id", how="left", indicator=True)
no_orders = merged2[merged2["_merge"] == "left_only"]
print(f"\nCustomers with no orders: {len(no_orders)}")
print(no_orders[["customer_id", "name"]])

# ── Check 3: Enrich and validate across tables ─────────────────────────────────
full = pd.merge(orders, customers, on="customer_id", how="inner")
print(f"\nValid orders: {len(full)}")

# Total spent per customer
spending = full.groupby("name")["amount"].sum().sort_values(ascending=False)
print(spending)

# ── Check 4: Concatenating datasets from multiple sources ──────────────────────
orders_jan = pd.DataFrame({"order_id": [201, 202], "amount": [100, 200]})
orders_feb = pd.DataFrame({"order_id": [203, 204], "amount": [150, 175]})

all_orders = pd.concat([orders_jan, orders_feb], ignore_index=True)
print(all_orders)
print(f"Duplicates after concat: {all_orders.duplicated(subset=['order_id']).sum()}")
```

**Practice tasks:**
1. Create a `products` table and an `order_items` table — check that all `product_id` values in `order_items` exist in `products`
2. Using the banklist, imagine you have a separate `acquirers` table. How would you check referential integrity?
3. What is the difference between a left join and an inner join for DQC purposes? Write 2 sentences
4. Merge two DataFrames and find rows that changed between two snapshots of the same data
5. Concatenate 3 monthly CSV files and verify no `order_id` appears in more than one file

---

## Lesson 12 — Reporting Your Findings

**Goal:** Turn audit results into clear, shareable reports.

```python
import pandas as pd

df = pd.read_csv("dataset/banklist.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df["closing_date"] = pd.to_datetime(df["closing_date"], errors="coerce")
df["year"]         = df["closing_date"].dt.year

# ── Text Summary Report ───────────────────────────────────────────────────────
def text_report(df: pd.DataFrame, name: str = "Dataset") -> None:
    sep = "=" * 50
    print(f"\n{sep}\n  DATA QUALITY SUMMARY — {name.upper()}\n{sep}")
    print(f"  Total rows     : {len(df):,}")
    print(f"  Total columns  : {len(df.columns)}")
    print(f"\n  Missing values (columns with nulls):")
    nulls = df.isnull().sum()
    for col, n in nulls[nulls > 0].items():
        pct = n / len(df) * 100
        print(f"    {col:<30} {n:>5} ({pct:.1f}%)")
    print(f"\n  Duplicate rows : {df.duplicated().sum()}")
    print(sep)

text_report(df, "Bank Failure List")

# ── Excel Report with multiple sheets ─────────────────────────────────────────
writer = pd.ExcelWriter("bank_quality_report.xlsx", engine="openpyxl")

# Sheet 1: cleaned data
df.to_excel(writer, sheet_name="Data", index=False)

# Sheet 2: failures by year
by_year = df.groupby("year")["bank_name"].count().reset_index()
by_year.columns = ["Year", "Failures"]
by_year.to_excel(writer, sheet_name="By Year", index=False)

# Sheet 3: failures by state
by_state = df.groupby("st")["bank_name"].count().reset_index()
by_state.columns = ["State", "Failures"]
by_state = by_state.sort_values("Failures", ascending=False)
by_state.to_excel(writer, sheet_name="By State", index=False)

# Sheet 4: null report
null_report = pd.DataFrame({
    "Column":   df.isnull().sum().index,
    "Null Count": df.isnull().sum().values,
    "Null %":   (df.isnull().sum() / len(df) * 100).round(2).values,
})
null_report.to_excel(writer, sheet_name="Null Report", index=False)

writer.close()
print("Report saved: bank_quality_report.xlsx")

# ── HTML Report (ydata-profiling) ─────────────────────────────────────────────
# pip install ydata-profiling
# from ydata_profiling import ProfileReport
# profile = ProfileReport(df, title="Bank DQC Report", explorative=True)
# profile.to_file("bank_report.html")
```

**Practice tasks:**
1. Run the full text report on the banklist
2. Generate the Excel report — open it and review each sheet
3. Add a 5th sheet called `"Issues"` that lists every quality issue found
4. Modify `text_report()` to also print the top 3 most common values for each object column
5. Write a function `compare_reports(df_before, df_after)` that shows what changed after cleaning

---

## Final Challenge — End-to-End DQC Project

Put every lesson together in one script. Use the banklist dataset.

**Requirements:**
1. Load the raw CSV
2. Run a full audit — log all issues by dimension and severity
3. Clean the data (fix types, handle nulls, remove duplicates, normalize strings)
4. Run the audit again on the cleaned data — show improvement
5. Answer 5 business questions using groupby:
   - Which year had the most failures?
   - Which state had the most failures?
   - Which acquirer took over the most banks?
   - What was the average time between closing and update?
   - How many banks were listed as "No Acquirer"?
6. Export: `banklist_clean.csv`, `audit_before.csv`, `audit_after.csv`, and a final `summary.xlsx`

When you can complete this challenge from memory, you are ready for the Data Quality Control Associate role.

---

*Lessons designed for: Data Quality Control Associate job prep | April 2026*
