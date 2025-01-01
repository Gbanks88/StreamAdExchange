# wsgi.py - Production server entry point
from app import create_app
application = create_app()

# run.py - Development server entry point
from app import create_app
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
