from amazon_advertising_api_sdk import AdvertisingApiClient

class AmazonAdvertising:
    def __init__(self, client_id, client_secret, region):
        self.client = AdvertisingApiClient(
            client_id=client_id,
            client_secret=client_secret,
            region=region
        )

    def setup_campaign(self, campaign_data):
        try:
            response = self.client.campaigns.create_campaign(campaign_data)
            return response
        except Exception as e:
            print(f"Error creating campaign: {e}")
            return None 