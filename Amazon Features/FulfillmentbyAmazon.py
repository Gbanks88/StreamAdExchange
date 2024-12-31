from sp_api.api import Orders, Inventory, FulfillmentInbound, FulfillmentOutbound
from sp_api.base import Marketplaces
import sys

sys.path.append('/path/to/your/module')  # Adjust the path accordingly

class AmazonFBA:
    def __init__(self, credentials):
        self.credentials = credentials
        self.marketplace = Marketplaces.US  # or your specific marketplace

    def get_inventory(self):
        try:
            inventory_api = Inventory(credentials=self.credentials)
            response = inventory_api.get_inventory_summary_marketplace()
            return response.payload
        except Exception as e:
            print(f"Error getting inventory: {e}")
            return None

    def create_inbound_shipment(self, shipment_data):
        try:
            fba_inbound = FulfillmentInbound(credentials=self.credentials)
            response = fba_inbound.create_inbound_shipment_plan(shipment_data)
            return response.payload
        except Exception as e:
            print(f"Error creating shipment: {e}")
            return None

    def get_orders(self, created_after):
        try:
            orders_api = Orders(credentials=self.credentials)
            response = orders_api.get_orders(CreatedAfter=created_after)
            return response.payload
        except Exception as e:
            print(f"Error getting orders: {e}")
            return None
   