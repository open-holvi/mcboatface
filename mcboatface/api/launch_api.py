from flask import Flask
from api.v1.blueprints import app as api_v1
from settings import UPLOAD_FOLDER



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.register_blueprint(api_v1, url_prefix='/api/v1')

if __name__ == "__main__":
    app.run('0.0.0.0', 8000)
