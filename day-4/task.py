#Practical Examples
#Example 1: Import CSV and Filter
import pandas as pd

df = pd.read_csv('sales_data.csv')

# Filter where Sales > 1000
high_sales = df[df['Sales'] > 1000]

print(high_sales.head())
#Example 2: Group sales by product category
grouped = df.groupby('Category')['Sales'].sum()
print(grouped)
#Example 3: Filtering and grouping together
filtered = df[df['Region'] == 'North']
grouped = filtered.groupby('Product')['Profit'].mean()
print(grouped)