from flask import Blueprint
from flask_restful import Api
from resources.Hello import Hello
from resources.Users import UserResource
from resources.Projects import ProjectResource
from resources.Actions import ActionResource

API_BP = Blueprint('api', __name__)
api = Api(API_BP)

api.add_resource(Hello, '/Hello')

# Add api routes for project end points
# Get
api.add_resource(ProjectResource, "/projects", "/projects/<int:project_id>", "/projects?search=<string:term>", "/projects?offset=<int:offsetValue>&limit=<int:limitValue>")
# Post
api.add_resource(ProjectResource, '/projects', endpoint = 'post')
# # Put
api.add_resource(ProjectResource, '/projects/<int:project_id>', endpoint = 'put')
# # Patch
api.add_resource(ProjectResource, '/projects/<int:project_id>', endpoint = 'patch')
# # Delete
api.add_resource(ProjectResource, '/projects/<int:project_id>', endpoint = 'delete')


# User api endpoints
# register
api.add_resource(UserResource, '/users/register', endpoint = 'userpost')

# Auth api endpoint
api.add_resource(UserResource, '/users/auth', endpoint = 'get_token')

# Action endpoint
api.add_resource(ActionResource, '/projects/<int:project_id>/actions', endpoint = 'actionpost')
api.add_resource(ActionResource, "/actions", "/projects/<int:project_id>/actions", "/actions/<int:action_id>", "/projects/<int:project_id>/actions/<int:action_id>")
api.add_resource(ActionResource, "/projects/<int:project_id>/actions/<int:action_id>", endpoint = 'actionput')
api.add_resource(ActionResource, "/projects/<int:project_id>/actions/<int:action_id>", endpoint = 'actiondelete')
