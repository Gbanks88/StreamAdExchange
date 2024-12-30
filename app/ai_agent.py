try:
    from uagents import Agent, Context, Model
    from uagents.setup import fund_agent_if_low
    AI_ENABLED = True
except ImportError:
    print("Warning: uagents not installed, running in fallback mode")
    AI_ENABLED = False
    
from datetime import datetime
import random
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if AI_ENABLED:
    class MarketData(Model):
        price: float
        volume: float
        timestamp: str
        prediction: str
        confidence: float

    # Create AI trading agent
    try:
        trading_agent = Agent(
            name="trading_assistant",
            port=8000,
            endpoint=["http://127.0.0.1:8000/submit"],
            seed="trading_agent_seed_123"
        )
        logger.info("Trading agent created successfully")
    except Exception as e:
        logger.error(f"Failed to create trading agent: {e}")
        AI_ENABLED = False
else:
    # Fallback implementation
    class MarketData:
        def __init__(self, price, volume, timestamp, prediction, confidence):
            self.price = price
            self.volume = volume
            self.timestamp = timestamp
            self.prediction = prediction
            self.confidence = confidence

    trading_agent = None

# Store market data
market_data = []
MAX_DATA_POINTS = 1000

def simulate_market_data():
    current_price = 100 + random.uniform(-5, 5)
    current_volume = 1000 + random.uniform(-100, 100)
    
    data = MarketData(
        price=current_price,
        volume=current_volume,
        timestamp=datetime.now().isoformat(),
        prediction="uptrend" if current_price > 100 else "downtrend",
        confidence=random.uniform(0.6, 0.9)
    ) if AI_ENABLED else MarketData(
        current_price,
        current_volume,
        datetime.now().isoformat(),
        "uptrend" if current_price > 100 else "downtrend",
        random.uniform(0.6, 0.9)
    )
    
    if len(market_data) >= MAX_DATA_POINTS:
        market_data.pop(0)
    market_data.append(data)
    return data

# Get latest market data with error handling
def get_latest_market_data():
    try:
        if not market_data:
            return simulate_market_data()
        return market_data[-1]
    except Exception as e:
        logger.error(f"Error getting latest market data: {e}")
        return None

# Initialize agent
try:
    fund_agent_if_low(trading_agent.wallet.address())
    logger.info(f"Agent funded successfully at address: {trading_agent.wallet.address()}")
except Exception as e:
    logger.error(f"Failed to fund agent: {e}") 