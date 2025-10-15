from flask import Flask
from routes.health import bp as health_bp
from routes.generate import bp as generate_bp
from routes.exports import bp as export_bp
from routes.web import bp as web_bp
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    # ADD THESE LINES - Tell Flask where templates are
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    print(f"🔍 Looking for templates in: {template_dir}")
    
    app = Flask(__name__, template_folder=template_dir)  # ADD template_folder
    
    app.register_blueprint(health_bp, url_prefix="/health")
    app.register_blueprint(generate_bp, url_prefix="/generate")
    app.register_blueprint(export_bp, url_prefix="/runs")
    app.register_blueprint(web_bp)
    return app

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app = create_app()
    app.run(debug=True, port=port)