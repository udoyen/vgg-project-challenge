from flask import request
from flask_restful import Resource
from Model import db, User, UserSchema
import secrets

users_schema = UserSchema(many=True)
user_schema = UserSchema()

class UserResource(Resource):

    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # validate and deserialize input
        data, errors = user_schema.load(json_data)
        if errors:
            return errors, 422
        user = User.query.filter_by(username=data['username']).first()
        if user:
            return {'message': 'User already exists'}, 400
        user = User(
            username=json_data['username'],
            password=json_data['password']
        )
        db.session.add(user)
        db.session.commit()

        result = user_schema.dump(user).data
        return {
            'status': 'success',
            'data': result
        }, 201

    def get(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # validate and deserialize input
        data, errors = user_schema.load(json_data)
        if errors:
            return errors, 422
        user = User.query.filter_by(username=data['username']).first()
        if user:
            return {'message': self.generate_user_token()}, 200
        else:
            return {'message': 'Unauthorized'}, 400

    def generate_user_token(self):
        sec = secrets.token_hex(16)
        return sec
