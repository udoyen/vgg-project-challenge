from flask import request
from flask_restful import Resource
from  Model import db, Project, ProjectSchema

projects_schema = ProjectSchema(many=True)
project_schema = ProjectSchema()

class ProjectResource(Resource):
    """
    Get all projects in the database
    """
    def get(self):
        projects = Project.query.all()
        projects = projects_schema.dump(projects).data
        return {'status': 'success', 'data': projects}, 200

    """
    Get project by id
    """
    def get_by_id(self, projectId):
        project = Project.query.filter_by(id=projectId).first()
        project = projects_schema.dump(project).data
        return {'status': 'success', 'data': project}, 200

    def post(self):
        json_data = request.get_json(force=True)
        # Return a 400 error if no input data
        # was provided
        if not json_data:
            return {'message': 'No inpute data provided'}, 400
        # Validate  and deserialize input
        data, errors = project_schema.load(json_data)
        if errors:
            return errors, 422
        project = Project.query.filter_by(name=data['name']).first()
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

        result = project_schema.dump(project).data
        return {
            "status": 'success',
            "data": result
        }, 201

    def put(self, projectId):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400

        # Validate and deserialize input
        data, errors = project_schema.load(json_data)
        if errors:
            return errors, 422
        project = Project.query.filter_by(id=data['id']).first()
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

        result = project_schema.dump(project).data
        return {'status': 'success', 'data': result}, 204

    def patch(self, projectId):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400

        # Validate and deserialize input
        data, errors = project_schema.load(json_data)
        if errors:
            return errors, 422
        project = Project.query.filter_by(id=data['id']).first()
        if not project:
            return {'message': 'Project does not exist'}, 400
        # Set the new values
        if project.name != data['name']:
            project.name = data['name']
        if project.description != data['description']:
            project.description = data['description']
        if project.completed != data['completed']:
            project.completed = data['completed']
        # commit the changes
        db.session.commit()

        result = project_schema.dump(project).data
        return {'status': 'success', 'data': result}, 204


    def delete(self, projectId):
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        data , errors = project_schema.load(json_data)
        if errors:
            return errors, 422
        project = Project.query.filter_by(id=data['id']).delete()
        db.session.commit()

        result = project_schema.dump(project).data

        return {'status': 'success', 'data': result}, 204
