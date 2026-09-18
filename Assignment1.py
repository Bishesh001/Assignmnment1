import pandas as pd

# 1. Read the CSV file
df = pd.read_csv(r"C:\Users\NIC\Downloads\pandas_dataset.csv")
print(df.head(5))

shape_before = df.shape

# 2. Rename columns: strip spaces, lowercase, underscores
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# 3. Drop the blank row sitting under the header, reset index
df = df.dropna(how="all").reset_index(drop=True)

# 4. Drop columns (if needed)
# Kept all columns — order_id/customer_name identify the record,
# category/product/city describe it, quantity/unit_price/discount feed
# into total_amount, and status/sales/profit drive the filters below.
# Nothing here is redundant enough to drop.

# 5. Count missing values
print(df.isnull().sum())

# 6a. Drop rows where sales is missing
df = df.dropna(subset=["sales"]).reset_index(drop=True)

# 6b. Fill missing values
df["profit"] = df["profit"].fillna(df["profit"].mean())
df["discount"] = df["discount"].fillna(df["discount"].median())

# 7. Fill missing customer_name
df["customer_name"] = df["customer_name"].fillna("Unknown")

# 8. Detect and remove duplicates based on order_id
dupe_mask = df.duplicated(subset=["order_id"])
n_duplicates = dupe_mask.sum()
print(f"Duplicates found: {n_duplicates}")
print(df[dupe_mask])

df = df.drop_duplicates(subset=["order_id"]).reset_index(drop=True)

# 9. Filtering and new columns
print(df[df["unit_price"] > 20000])

print(df.loc[(df["unit_price"] > 10000) & (df["status"] == "Completed"),
             ["customer_name", "category", "status"]])

df["total_amount"] = df["quantity"] * df["unit_price"] - df["discount"]
df["customer_type"] = df["quantity"].apply(
    lambda q: "Bulk Buyer" if q >= 3 else "Regular Buyer"
)

# 10. Final clean dataset
shape_after = df.shape
print("Before:", shape_before, "After:", shape_after)
print(df.head(10))