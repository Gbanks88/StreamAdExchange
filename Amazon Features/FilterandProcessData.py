import pandas as pd

# Example data for deals
deals = {
    'deal_id': [1, 2, 3],
    'description': ['Deal 1', 'Deal 2', 'Deal 3'],
    'discount': ['10%', '20%', 'No Discount']
}

# Create DataFrame from deals
df = pd.DataFrame(deals)

# Filter the DataFrame to get deals with discounts
filtered_deals = df[df['discount'].str.contains('%')]
print(filtered_deals)

filtered_deals.to_csv('filtered_deals.csv', index=False)