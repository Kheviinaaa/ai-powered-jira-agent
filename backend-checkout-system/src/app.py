from flask import Flask
from flask_cors import CORS
import logging

def create_app():
    app = Flask(__name__)
    
    # Configure CORS for local development
    CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Import and register blueprints
    from routes.health import bp as health_bp
    from routes.generate import bp as gen_bp
    from routes.epics import bp as epics_bp
    from routes.exports import bp as exp_bp
    
    app.register_blueprint(health_bp)
    app.register_blueprint(gen_bp, url_prefix="/api/generate")
    app.register_blueprint(epics_bp, url_prefix="/api/epics")
    app.register_blueprint(exp_bp, url_prefix="/api/runs")
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(port=5000, debug=True)
