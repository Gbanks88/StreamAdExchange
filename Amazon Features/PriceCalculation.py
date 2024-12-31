def calculate_total_cost(purchase_price, shipping_cost, amazon_fees):
    total_cost = purchase_price + shipping_cost + amazon_fees
    return total_cost

# Call the function and print the result
total_cost = calculate_total_cost(50, 10, 5)
print(total_cost)