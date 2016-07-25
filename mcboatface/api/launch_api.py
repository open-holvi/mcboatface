from flask import Flask
from api.v1.blueprints import app as api_v1

app = Flask(__name__)
app.register_blueprint(api_v1, url_prefix='/api/v1')

if __name__ == "__main__":
    app.run('0.0.0.0', 8000)
