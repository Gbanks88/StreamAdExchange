from app import create_app
import os

# Create app with development configuration
app = create_app('development')

if __name__ == '__main__':
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5001)),
        debug=True
    )
      