from fetchai.ledger.contract import Contract
from fetchai.ledger.crypto import Entity

# Create a contract owner entity
contract_owner = Entity()

contract_code = """
@action
function place_ad(ad_id: String, advertiser: Address, amount: Int64)
  var existing_balance = State<Int64>("balance");
  existing_balance = existing_balance.get(advertiser, 0);
  existing_balance.set(advertiser, existing_balance.get() + amount);
endfunction
"""

# Initialize contract with owner
contract = Contract(contract_code, contract_owner)
