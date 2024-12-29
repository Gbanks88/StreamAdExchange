# Mock Balt Integration
def process_payment(user_id, amount, payment_method):
    """
    Mock function to simulate payment processing
    """
    return {
        "status": "success",
        "transaction_id": "mock_tx_123",
        "user_id": user_id,
        "amount": amount,
        "payment_method": payment_method,
        "timestamp": "2024-01-01T00:00:00Z"
    }

# Example usage
user_id = 'user_123'
amount = 100  # Amount in USD
payment_method = 'crypto'  # or 'stocks'

payment_result = process_payment(user_id, amount, payment_method)
print(f"Payment Result: {payment_result}")
