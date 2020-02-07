from flask_restful import Resource

class ActionResource(Resource):
    def get(self):
        return {'message': 'Hello from actions'}