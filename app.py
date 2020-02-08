from flask import Blueprint
from flask_restful import Api
from resources.Hello import Hello
from resources.Users import UserResource
from resources.Projects import ProjectResource
from resources.Actions import ActionResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(Hello, '/Hello')

# Add api routes for project end points
# Get
api.add_resource(ProjectResource, "/projects", "/projects/<int:project_id>")
# Get by id
# api.add_resource(ProjectResource, '/projects/<int:project_id>', endpoint = 'get_user')
# Post
api.add_resource(ProjectResource, '/projects', endpoint = 'post')
# Put
api.add_resource(ProjectResource, '/projects/<int:project_id>', endpoint = 'put')
# Patch
api.add_resource(ProjectResource, '/projects/<int:project_id>', endpoint = 'patch')
# Delete
api.add_resource(ProjectResource, '/projects/<int:project_id>', endpoint = 'delete')

# User api endpoints
# register
api.add_resource(UserResource, '/users/register', endpoint = 'userpost')

# Auth api endpoint
api.add_resource(UserResource, '/users/auth', endpoint = 'get_token')