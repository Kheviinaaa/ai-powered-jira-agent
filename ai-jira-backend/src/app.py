from flask import Flask
from .routes.health import bp as health_bp
from .routes.generate import bp as generate_bp
from .routes.exports import bp as export_bp
from dotenv import load_dotenv
import os

load_dotenv()  # load .env

def create_app():
    app = Flask(__name__)
    app.register_blueprint(health_bp, url_prefix="/health")
    app.register_blueprint(generate_bp, url_prefix="/generate")
    app.register_blueprint(export_bp, url_prefix="/runs")
    return app

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app = create_app()
    app.run(debug=True, port=port)

