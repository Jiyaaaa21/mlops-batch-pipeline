import pandas as pd

df = pd.read_csv("data.csv", header=None)

# Split and clean
df = df[0].str.replace('"', '').str.split(",", expand=True)

# Set column names from first row
df.columns = df.iloc[0]

# Remove the first row (header row inside data)
df = df[1:].reset_index(drop=True)

# Convert numeric columns
numeric_cols = ["open", "high", "low", "close", "volume_btc", "volume_usd"]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col])

print(df.head())
print(df.columns)
print(df.shape)
print(df["close"].isnull().sum())