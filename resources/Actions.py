from flask import request
from flask_restful import Resource
from model import db, Action, ActionSchema, Project, ProjectSchema

ACTIONS_SCHEMA = ActionSchema(many=True)
ACTION_SCHEMA = ActionSchema()

class ActionResource(Resource):
    def get(self):
        json_data = request.get_json(force=True)
        if not json_data:
            return {"message": "No input data provided"}, 400
        return {'message': 'Hello from actions'}

    def post(self, project_id=None):
        json_data = request.get_json(force=True)
        if not json_data:
            return {"message": "No input data provided"}, 400
        # validate and deserialize input
        data, errors = ACTION_SCHEMA.load(json_data)
        if errors:
            return errors, 500
        # check to make sure the project_id exists
        project = Project.query.filter_by(id=project_id).first()
        if project and project_id is not None and json_data['project_id'] == project_id:
            action = Action(
                project_id=json_data['project_id'],
                description=json_data['description'],
                note=json_data['note']
            )
            db.session.add(action)
            db.session.commit()

            result = ACTION_SCHEMA.dump(action).data
            return {
                "status": 'success',
                "data": result

            }, 200
        else:
            return {
                "status": 'Resource not foung',
            }, 400
