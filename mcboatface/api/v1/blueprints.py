"""V1 for api."""

import tempfile
from service import health_checks
from service.face_comparison import FaceRepresentationService
from api.utils import allowed_file
from flask import Blueprint, jsonify, request, make_response, abort

from settings import UPLOAD_FOLDER

# Booting up service uppon api start.
service = FaceRepresentationService()

app = Blueprint('api_v1', __name__)

@app.route("/health/status")
def health_status():
    """Return system satus."""
    return jsonify(**health_checks.system_status())

@app.route("/face/representation", methods=['POST'])
def get_representation():
    """
    Return the face (main one) on the uploaded image.
    :param: file image
    :return: {'face': {...} }
    """
    if request.method == 'POST':
        # check if the post request has the file part
        if 'image' not in request.files:
            abort(422)
        file = request.files['image']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            abort(422)

        if file and allowed_file(file.filename):
            image_file = tempfile.NamedTemporaryFile()
            image_file.seek(0)
            file.save(image_file.name)
            image_file.seek(0)
            result = service.get_image_representation(image_file.name)
            if result is not None:
                return jsonify(
                    {'face': service.get_absolute_representation(result)})
        else:
            abort(401)

    return make_response("Unable to find face", 404)


@app.route("/faces/representation", methods=['POST'])
def get_representations():
    """
    Return the face (main one) on the uploaded image.
    :param: file image
    :return: {'faces': [{...}, {...}] }
    """
    if request.method == 'POST':
        # check if the post request has the file part
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['image']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            abort(422)

        if file and allowed_file(file.filename):
            image_file = tempfile.NamedTemporaryFile()
            image_file.seek(0)
            file.save(image_file.name)
            image_file.seek(0)
            result = service.get_all_representations(image_file.name)
            if result is not None:
                return jsonify({
                    'faces': list(
                        (service.get_absolute_representation(r)
                         for r in result))})
        else:
            abort(401)

    return make_response("Unable to find faces", 404)


@app.route("/id_selfie/score", methods=['POST'])
def score_selfie_photo():
    """
    Return the face (main one) on the uploaded image.
    :param: file image
    :return: {'score': x.xxx }
    """
    if request.method == 'POST':
        # check if the post request has the file part
        if 'image' not in request.files:
            abort(422)
        file = request.files['image']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            abort(422)

        if file and allowed_file(file.filename):
            image_file = tempfile.NamedTemporaryFile()
            image_file.seek(0)
            file.save(image_file.name)
            image_file.seek(0)
            result = service.get_all_representations(image_file.name)

            if len(result) != 2:
                return make_response(
                    "%s (not two) faces where found in the image"
                    % len(result), 422)

            final_result = {
                'score': service.compare_representations(result[0], result[1])
            }
            return jsonify(final_result)
        else:
            abort(401)

    return make_response("Unable to find faces", 404)
