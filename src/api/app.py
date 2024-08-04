from flask import Flask
from flask_cors import CORS
def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__)

    # Import and register the routes
    from src.api.endpoints import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)  # Run the app on all available IPs
