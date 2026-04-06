"""
Pandas practice using dataset/banklist.csv
Run each section independently to learn each concept.
"""

import pandas as pd

# ── 1. Load & First Look ────────────────────────────────────────────────────
df = pd.read_csv("dataset/banklist.csv")
print(df.shape)
print(df.dtypes)
print(df.head())

# ── 2. Clean Column Names ───────────────────────────────────────────────────
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
print(df.columns.tolist())

# ── 3. Parse Dates ──────────────────────────────────────────────────────────
df["closing_date"] = pd.to_datetime(df["closing_date"], format="%d-%b-%y")
df["updated_date"] = pd.to_datetime(df["updated_date"], format="%d-%b-%y")
df["closing_year"]  = df["closing_date"].dt.year
df["closing_month"] = df["closing_date"].dt.month

# ── 4. Selecting Data ───────────────────────────────────────────────────────
print(df[["bank_name", "st", "closing_date"]].head())
print(df.iloc[0:3, 0:3])
print(df.loc[0, "bank_name"])

# ── 5. Filtering ────────────────────────────────────────────────────────────
ga_banks    = df[df["st"] == "GA"]
post_2010   = df[df["closing_year"] > 2010]
no_buyer    = df[df["acquiring_institution"] == "No Acquirer"]
southeast   = df[df["st"].isin(["FL", "GA", "CA"])]
first_banks = df[df["bank_name"].str.contains("First", case=False, na=False)]
crisis      = df[df["closing_year"].between(2008, 2010)]

print(f"Georgia failures: {len(ga_banks)}")
print(f"No acquirer: {len(no_buyer)}")
print(f"'First' in name: {len(first_banks)}")

# ── 6. Sorting ──────────────────────────────────────────────────────────────
print(df.sort_values("closing_date").head(3))
print(df.sort_values(["st", "closing_date"]).head(5))

# ── 7. Descriptive Statistics ───────────────────────────────────────────────
print(df["closing_year"].value_counts().sort_index())
print(df["st"].value_counts().head(10))
print(f"Unique states: {df['st'].nunique()}")

# ── 8. GroupBy ──────────────────────────────────────────────────────────────
by_state = df.groupby("st").size().sort_values(ascending=False)
print(by_state.head(10))

by_year = df.groupby("closing_year").agg(
    total=("bank_name", "count"),
    first=("closing_date", "min"),
    last=("closing_date", "max"),
)
print(by_year)

# ── 9. Pivot Table ──────────────────────────────────────────────────────────
pivot = df.pivot_table(
    index="closing_year",
    columns="st",
    values="bank_name",
    aggfunc="count",
    fill_value=0,
)
# Top 5 worst years nationally
print(pivot.sum(axis=1).sort_values(ascending=False).head(5))

# ── 10. Adding Columns ──────────────────────────────────────────────────────
df["days_to_update"] = (df["updated_date"] - df["closing_date"]).dt.days
df["is_crisis_era"]  = df["closing_year"].between(2008, 2012)
df["location"]       = df["city"] + ", " + df["st"]

print(df[["bank_name", "days_to_update", "is_crisis_era", "location"]].head())

# ── 11. Missing Data ────────────────────────────────────────────────────────
print(df.isnull().sum())
df["acquiring_institution"] = df["acquiring_institution"].fillna("Unknown")

# ── 12. Apply & Map ─────────────────────────────────────────────────────────
region_map = {
    "GA": "South", "FL": "South", "AL": "South", "MS": "South",
    "CA": "West",  "OR": "West",  "WA": "West",
    "NY": "Northeast", "NJ": "Northeast", "CT": "Northeast",
    "IL": "Midwest", "OH": "Midwest", "MI": "Midwest",
}
df["region"] = df["st"].map(region_map).fillna("Other")

def era_label(year):
    if 2008 <= year <= 2012:
        return "Financial Crisis"
    elif year < 2008:
        return "Pre-Crisis"
    return "Post-Crisis"

df["era"] = df["closing_year"].apply(era_label)
print(df["era"].value_counts())

# ── 13. String Methods ──────────────────────────────────────────────────────
print(df["bank_name"].str.len().describe())
print(df["bank_name"].str.startswith("First").sum(), "banks start with 'First'")

# ── 14. Datetime Accessors ──────────────────────────────────────────────────
print(df["closing_date"].dt.day_name().value_counts())  # which weekday?
print(df["closing_date"].dt.quarter.value_counts().sort_index())

# ── 15. Time Series Resampling ──────────────────────────────────────────────
ts = df.set_index("closing_date").sort_index()
monthly = ts["bank_name"].resample("ME").count()
print(monthly.tail(12))

# Rolling 12-month total
print(monthly.rolling(12).sum().dropna().tail(12))

# ── 16. Chaining ────────────────────────────────────────────────────────────
result = (
    df
    .query("closing_year >= 2008 and closing_year <= 2012")
    .groupby(["closing_year", "st"])
    .size()
    .reset_index(name="failures")
    .sort_values("failures", ascending=False)
    .head(10)
)
print(result)

# ── 17. Export ──────────────────────────────────────────────────────────────
# df.to_csv("output/cleaned_banklist.csv", index=False)
# pivot.to_csv("output/failures_by_year_state.csv")
