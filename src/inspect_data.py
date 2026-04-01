import pandas as pd

file_path = "data/Statistical Tables (2020 CBPP Subnational).xlsx"

df = pd.read_excel(file_path, sheet_name="Table 2")

# Fix headers
df.columns = df.iloc[1]

# Remove header rows
df = df[3:]

# Rename columns
df.columns = ["Region", "2020-2025", "2025-2030", "2030-2035"]

# Drop rows where ALL values are NaN
df = df.dropna(how="all")

# Strip whitespace
df["Region"] = df["Region"].astype(str).str.strip()

# Remove rows that are not actual regions
df = df[df["Region"] != "nan"]

# Remove "PHILIPPINES" to only include regions
df = df[df["Region"] != "PHILIPPINES"]

df["avg_growth"] = df[["2020-2025", "2025-2030", "2030-2035"]].mean(axis=1)

def classify_growth(rate):
    if rate > 1.0:
        return "High Growth"
    elif rate > 0.6:
        return "Moderate Growth"
    else:
        return "Low Growth"

df["growth_category"] = df["avg_growth"].apply(classify_growth)

# Remove rows that contain "Source"
df = df[~df["Region"].str.contains("Source", na=False)]

# Reset index
df = df.reset_index(drop=True)

print(df)

# Remove unwanted rows (Source, Table, etc.)
df = df[
    (~df["Region"].str.contains("Source", na=False)) &
    (~df["Region"].str.contains("Table", na=False))
]

# Convert to CSV and save to data folder
df.to_csv("data/clean_population_growth.csv", index=False)
print("Dataset saved")