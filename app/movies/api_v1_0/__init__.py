from flask import Blueprint

api_v1_0_bp = Blueprint('api_v1_0_bp', __name__)

from .resources.resource_user import UserListResource, UserResource, Auth

