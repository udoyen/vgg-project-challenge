from flask import Blueprint
from flask_restful import Api
from resources.Hello import Hello
# from resources.Users import Users
# from resources.Projects import Projects
# from resources.Actions import Actions

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(Hello, '/Hello')
