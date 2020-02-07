from flask import Blueprint
from flask_restful import Api
from resources.Hello import Hello
from resources.Users import User
from resources.Projects import Project
from resources.Actions import Action

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(Hello, '/Hello')

# Add api routes for project end points
# Get
api.add_resource(Project, '/projects', endpoint = 'get')
# Get by id
api.add_resource(Project, '/projects/<int:id>', endpoint = 'get_by_id')
# Post
api.add_resource(Project, '/projects', endpoint = 'post')
# Put
api.add_resource(Project, '/projects/<int:id>', endpoint = 'put')
# Patch
api.add_resource(Project, '/projects/<int:id>', endpoint = 'patch')
# Delete
api.add_resource(Project, '/projects/<int:id>', endpoint = 'delete')