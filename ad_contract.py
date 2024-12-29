from fetchai.ledger.contract import Contract

contract_code = """
@action
function place_ad(ad_id: String, advertiser: Address, amount: Int64)
  var existing_balance = State<Int64>("balance");
  existing_balance = existing_balance.get(advertiser, 0);
  existing_balance.set(advertiser, existing_balance.get() + amount);
endfunction
"""

contract = Contract(contract_code)
