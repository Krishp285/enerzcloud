# Practical Examples
# Example 1: Detect and Fill Nulls
import pandas as pd

df = pd.DataFrame({
    'Name': ['Alice', 'Bob', None, 'David'],
    'Age': [25, None, 35, 40]
})

print("Before filling nulls:")
print(df)

df['Name'].fillna('Unknown', inplace=True)
df['Age'].fillna(df['Age'].mean(), inplace=True)

print("nAfter filling nulls:")
print(df)
# Example 2: Remove duplicate rows based on ‘Name’
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Alice', 'David'],
    'Age': [25, 30, 25, 40]
})

print("Before removing duplicates:")
print(df)

df = df.drop_duplicates(subset=['Name'])
print("nAfter removing duplicates:")
print(df)
# Example 3: Rename columns for clarity
df = pd.DataFrame({
    'Nm': ['Alice', 'Bob'],
    'Ag': [25, 30]
})

print("Before renaming:")
print(df)

df.rename(columns={'Nm': 'Name', 'Ag': 'Age'}, inplace=True)

print("nAfter renaming:")
print(df)