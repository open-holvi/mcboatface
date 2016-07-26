"""V1 for api."""

from service import health_checks
from service.face_comparison import FaceComparisonService
from flask import Blueprint, jsonify, request
import tempfile
from settings import ALLOWED_EXTENSIONS, UPLOAD_FOLDER

# Booting up service uppon api start.
service = FaceComparisonService()

app = Blueprint('api_v1', __name__)

@app.route("/health/status")
def health_status():
    """Return system satus."""
    return jsonify(**health_checks.system_status())


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/faces/representation", methods=['POST'])
def register_representation():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):

            image_file = tempfile.NamedTemporaryFile(
                dir=UPLOAD_FOLDER)
            image_file.seek(0)
            file.save(image_file.name)
            image_file.seek(0)
            return service.get_image_representation(image_file.name)
    return None
