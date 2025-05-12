from flask import Blueprint
scans_bp = Blueprint("scans", __name__)
from . import routes
