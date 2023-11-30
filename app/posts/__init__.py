from flask import Blueprint

posts = Blueprint('posts', __name__, template_folder="templates/posts")

from . import views