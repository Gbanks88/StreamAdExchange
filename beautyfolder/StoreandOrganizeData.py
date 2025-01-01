import pandas as pd

# Example DataFrame creation
deals = pd.DataFrame({
    'deal_id': [1, 2, 3],
    'description': ['Deal 1', 'Deal 2', 'Deal 3'],
    'active': [True, False, True]
})

# Filter the DataFrame to get active deals
filtered_deals = deals[deals['active'] == True]

filtered_deals.to_csv('deals.csv', index=False)

print("Data has been saved to deals.csv")