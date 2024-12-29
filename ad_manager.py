class AdManager:
    def __init__(self):
        self.ads = {}
        self.balances = {}
        self.initialize_demo_data()

    def initialize_demo_data(self):
        # Add some demo data
        self.ads = {
            "ad1": {
                "id": "ad1",
                "advertiser": "0x123",
                "amount": 1000,
                "status": "active"
            },
            "ad2": {
                "id": "ad2",
                "advertiser": "0x456",
                "amount": 2000,
                "status": "active"
            }
        }
        
        self.balances = {
            "0x123": 1000,
            "0x456": 2000
        }

    def place_ad(self, ad_id, advertiser, amount):
        if ad_id in self.ads:
            raise ValueError("Ad ID already exists")
        
        self.ads[ad_id] = {
            "id": ad_id,
            "advertiser": advertiser,
            "amount": amount,
            "status": "active"
        }
        
        # Update advertiser balance
        if advertiser not in self.balances:
            self.balances[advertiser] = 0
        self.balances[advertiser] += amount
        
        return self.ads[ad_id]

    def get_ads(self):
        return list(self.ads.values())

    def get_ad(self, ad_id):
        return self.ads.get(ad_id)

    def update_ad(self, ad_id, data):
        if ad_id not in self.ads:
            raise ValueError("Ad not found")
        
        self.ads[ad_id].update(data)
        return self.ads[ad_id]

    def delete_ad(self, ad_id):
        if ad_id not in self.ads:
            raise ValueError("Ad not found")
        
        del self.ads[ad_id]

    def get_active_ads(self):
        return [ad for ad in self.ads.values() if ad["status"] == "active"]

    def get_balance(self, address):
        return self.balances.get(address, 0)
