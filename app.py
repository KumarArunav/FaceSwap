
from flask import Flask
from routes import swap_faces_api_bp, swap_faces_client_bp

app = Flask(__name__)

# Register routes
app.register_blueprint(swap_faces_api_bp)
app.register_blueprint(swap_faces_client_bp)

if __name__ == '__main__':
    app.run(debug=True)

