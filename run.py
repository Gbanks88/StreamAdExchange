from app import create_app
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = create_app()

if __name__ == '__main__':
    try:
        logger.info("Starting the application...")
        port = int(os.getenv('FLASK_PORT', 5001))
        app.run(
            host='0.0.0.0',
            port=port,
            debug=True,
            use_reloader=True
        )
    except Exception as e:
        logger.error(f"Error starting app: {str(e)}", exc_info=True)
      