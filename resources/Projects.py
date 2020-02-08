from flask import request
from flask_restful import Resource
from model import db, Project, ProjectSchema

PROJECTS_SCHEMA = ProjectSchema(many=True)
PROJECT_SCHEMA = ProjectSchema()

class ProjectResource(Resource):
    """
    Get all projects in the database
    """
    def get(self, project_id=None):
        if project_id is not None:
            project = Project.query.filter_by(id = project_id).all()
            project = PROJECTS_SCHEMA.dump(project).data
            return {'status': 'success', 'data': project}, 200
        else:
            projects = Project.query.all()
            projects = PROJECTS_SCHEMA.dump(projects).data
            return {'status': 'success', 'data': projects}, 200

    def post(self):
        json_data = request.get_json(force=True)
        # Return a 400 error if no input data
        # was provided
        if not json_data:
            return {'message': 'No inpute data provided'}, 400
        # Validate  and deserialize input
        data, errors = PROJECT_SCHEMA.load(json_data)
        if errors:
            return errors, 422
        project = Project.query.filter_by(name=data['name']).all()
        # Check if that project already exists
        if project:
            return {'message': 'Project already exists'}, 400
        # if the project doesn't exist add it
        # to the database
        project = Project(
            name=json_data['name'],
            description=json_data['description'],
            completed=json_data['completed']
        )
        db.session.add(project)
        db.session.commit()

        result = PROJECT_SCHEMA.dump(project).data
        return {
            "status": 'success',
            "data": result
        }, 201

    def put(self, project_id):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400

        # Validate and deserialize input
        data, errors = PROJECT_SCHEMA.load(json_data)
        if errors:
            return errors, 422
        project = Project.query.filter_by(id=project_id).first()
        if not project:
            project = Project(
                name=json_data['name'],
                description=json_data['description'],
                completed=json_data['completed']
            )
            db.session.add(project)
            # return {'message': 'Project does not exist'}, 400
        else:
            # Set the new values
            project.name = data['name']
            project.description = data['description']
            project.completed = data['completed']
        # commit the changes
        db.session.commit()

        result = PROJECT_SCHEMA.dump(project).data
        return {'status': 'success', 'data': result}, 204

    def patch(self, project_id=None):
        json_data = request.get_json(force=True)

        if not json_data:
            return {'message': 'No input data provided'}, 400

        # Validate and deserialize input
        data, errors = PROJECT_SCHEMA.load(json_data)
        if errors:
            return errors, 422
        project = Project.query.filter_by(id=project_id).first()
        if not project:
            return {'message': 'Project does not exist'}, 400
        if project_id is not None:
            # Set the new values
            # commit the changes
            project.name = data['name']
            project.description = data['description']
            project.completed = data['completed']
            result = PROJECT_SCHEMA.dump(project).data
            db.session.commit()
            return {'status': 'success', 'data': result}, 200
        else:
            return json_data


    def delete(self, project_id=None):
        if project_id is not None:
            project = Project.query.filter_by(id=project_id).delete()
            result = PROJECT_SCHEMA.dump(project).data
            db.session.commit()
            return {'status': 'success', 'data': result}, 200
        else:
            return {'message': 'Project item could not be deleted!'}, 404


