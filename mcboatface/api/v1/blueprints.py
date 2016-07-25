"""V1 for api."""

from service import health_checks
from service.face_comparison import FaceComparisonService
from flask import Blueprint, jsonify


# Booting up service uppon api start.
service = FaceComparisonService()

app = Blueprint('api_v1', __name__)

@app.route("/health/status")
def health_status():
    """Return system satus."""
    return jsonify(**health_checks.system_status())


@app.route("/faces/register/<ext_reference>")
def register_representation(ext_reference):
    return "Hello %s" % ext_reference
