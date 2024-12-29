from fetchai.ledger.api import LedgerApi
from fetchai.ledger.crypto import Entity
from fetchai.ledger.contract import Contract

api = LedgerApi('127.0.0.1', 8000)
entity = Entity()
contract = Contract()

contract.create(api, entity)
