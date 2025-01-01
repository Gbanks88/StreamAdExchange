#### Step 3: Listing Products on Amazon
#1. **Listing Automation**:
 #  ```python
   # Use Amazon's MWS (Marketplace Web Service) or SP API (Selling Partner API) to automate listing
import os
from amazon.api import AmazonAPI

# Load credentials from environment variables
AMAZON_ACCESS_KEY = os.getenv('AMAZON_ACCESS_KEY')
AMAZON_SECRET_KEY = os.getenv('AMAZON_SECRET_KEY')
AMAZON_ASSOC_TAG = os.getenv('AMAZON_ASSOC_TAG')

amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG)
product = amazon.lookup(ItemId='B01N5IB20Q')
print(product.title)
