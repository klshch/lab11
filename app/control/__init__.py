from flask import Blueprint

control = Blueprint('control', __name__, template_folder="templates/control")

from . import views