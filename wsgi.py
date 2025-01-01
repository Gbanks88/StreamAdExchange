from app import create_app

application = create_app('default')  # Use 'default' configuration

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5001, debug=True) 