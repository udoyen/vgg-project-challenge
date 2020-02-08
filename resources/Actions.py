from flask import request
from flask_restful import Resource
from model import db, Action, ActionSchema, Project, ProjectSchema

ACTIONS_SCHEMA = ActionSchema(many=True)
ACTION_SCHEMA = ActionSchema()

class ActionResource(Resource):

    def get(self, project_id=None, action_id=None):
        if project_id is None and action_id is None:
            # get all actions
            actions = Action.query.all()
            actions = ACTIONS_SCHEMA.dump(actions).data
            return { "status": 'success', 'data': actions}, 200
        elif project_id is not None:
            # get all actions for a particular project
            actions = Action.query.filter_by(project_id=project_id).all()
            actions = ACTIONS_SCHEMA.dump(actions).data
            return {"status": 'success', 'data': actions}, 200
        elif action_id is not None:
            # get all the actions by action_id
            actions = Action.query.filter_by(id=action_id).all()
            actions = ACTIONS_SCHEMA.dump(actions).data
            return {"status": 'success', "data": actions}, 200
        elif action_id is not None and project_id is not None:
            # get a particular action using project and action id
            action = Action.query.filter_by(Action.id == action_id, Action.project_id == project_id)
            action = ACTIONS_SCHEMA.dump(actions).data
            return {"status": 'success', "data": action}, 200
        else:
            return { "status": 'Resource not found!'}, 404

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
                "status": 'Resource not found',
            }, 404

    def put(self, project_id=None, action_id=None):
        json_data = request.get_json(force=True)
        if not json_data:
            return {"message": "No input data provided"}, 400
        # Validate and deserialize input
        data, errors = ACTION_SCHEMA.load(json_data)
        if errors:
            return errors, 500
        if action_id is not None and project_id is not None:
            action = Action.query.filter_by(id=action_id, project_id=project_id).first()
            if not action:
                action = Action(
                    project_id=json_data['project_id'],
                    description=json_data['description'],
                    note=json_data['note']
                )
                db.session.add(action)
                db.session.commit()
                action = ACTION_SCHEMA.dump(action).data
                return {"status": "success", "data": action}, 200
            else:
                action.project_id = data['project_id']
                action.description = data['description']
                action.note = data['note']
                db.session.commit()
                action = ACTION_SCHEMA.dump(action)
                return {"status": "success", "data": action}, 200
        else:
            return {"status": "Resource not found"}, 404



