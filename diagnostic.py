import os
import sys
import logging
import importlib
import subprocess
from datetime import datetime

# Set up logging
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, f"diagnostic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)

class DiagnosticTool:
    def __init__(self):
        self.errors = []
        self.warnings = []
        
    def check_python_packages(self):
        logging.info("Checking Python packages...")
        required_packages = [
            'flask',
            'flask_caching',
            'flask_limiter',
            'python-dotenv',
            'redis',
            'uagents',
            'fetchai-ledger-api'
        ]
        
        for package in required_packages:
            try:
                importlib.import_module(package.replace('-', '_'))
                logging.info(f"✓ {package} is installed")
            except ImportError as e:
                error_msg = f"✗ {package} is not installed. Run: pip install {package}"
                self.errors.append(error_msg)
                logging.error(error_msg)

    def check_file_structure(self):
        logging.info("Checking file structure...")
        required_files = [
            'run.py',
            'app/__init__.py',
            'app/routes.py',
            'app/ai_agent.py',
            'app/extensions.py',
            'app/templates/base.html',
            'app/templates/service_detail.html',
            'app/static/js/main.js',
            'requirements.txt'
        ]
        
        for file_path in required_files:
            if not os.path.exists(file_path):
                error_msg = f"✗ Missing file: {file_path}"
                self.errors.append(error_msg)
                logging.error(error_msg)
            else:
                logging.info(f"✓ Found {file_path}")

    def check_flask_app(self):
        logging.info("Checking Flask application...")
        try:
            from app import create_app
            app = create_app()
            with app.test_client() as client:
                response = client.get('/')
                if response.status_code == 200:
                    logging.info("✓ Flask application is working")
                else:
                    error_msg = f"✗ Flask application returned status code {response.status_code}"
                    self.errors.append(error_msg)
                    logging.error(error_msg)
        except Exception as e:
            error_msg = f"✗ Flask application error: {str(e)}"
            self.errors.append(error_msg)
            logging.error(error_msg)

    def check_ai_integration(self):
        logging.info("Checking AI integration...")
        try:
            from app.ai_agent import AI_ENABLED, get_latest_market_data
            if AI_ENABLED:
                data = get_latest_market_data()
                if data:
                    logging.info("✓ AI agent is working")
                else:
                    self.warnings.append("⚠ AI agent returned no data")
                    logging.warning("AI agent returned no data")
            else:
                self.warnings.append("⚠ Running in fallback mode")
                logging.warning("Running in fallback mode")
        except Exception as e:
            error_msg = f"✗ AI integration error: {str(e)}"
            self.errors.append(error_msg)
            logging.error(error_msg)

    def check_javascript(self):
        logging.info("Checking JavaScript files...")
        js_file = 'app/static/js/main.js'
        if os.path.exists(js_file):
            with open(js_file, 'r') as f:
                content = f.read()
                if 'updateMarketData' not in content:
                    self.warnings.append("⚠ Market data update function missing in main.js")
                    logging.warning("Market data update function missing in main.js")
                else:
                    logging.info("✓ JavaScript functions present")
        else:
            error_msg = "✗ main.js file not found"
            self.errors.append(error_msg)
            logging.error(error_msg)

    def generate_report(self):
        logging.info("\n=== Diagnostic Report ===")
        
        if self.errors:
            logging.error("\nErrors found:")
            for error in self.errors:
                logging.error(error)
            
            logging.info("\nTo fix errors:")
            logging.info("1. Install missing packages: pip install -r requirements.txt")
            logging.info("2. Check the log file for specific error messages")
            logging.info("3. Verify file structure and permissions")
            logging.info("4. Check Flask application configuration")
            logging.info("5. Verify AI agent setup")
        
        if self.warnings:
            logging.warning("\nWarnings found:")
            for warning in self.warnings:
                logging.warning(warning)
        
        if not self.errors and not self.warnings:
            logging.info("\n✓ All checks passed successfully!")
        
        logging.info(f"\nDetailed log file: {log_file}")

    def run_all_checks(self):
        logging.info("Starting diagnostic checks...")
        self.check_python_packages()
        self.check_file_structure()
        self.check_flask_app()
        self.check_ai_integration()
        self.check_javascript()
        self.generate_report()

if __name__ == "__main__":
    tool = DiagnosticTool()
    tool.run_all_checks() 