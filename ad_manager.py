from fetchai.ledger.api import LedgerApi
from fetchai.ledger.crypto import Entity

api = LedgerApi('127.0.0.1', 8000)
entity = Entity()

balance = api.tokens.balance(entity)
print(f"Balance: {balance}")
