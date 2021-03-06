import os
from flask import Flask
from flask import  request
from flask_restful import Resource
import urllib.request
from sqlalchemy import update
from werkzeug.utils import secure_filename
from model import db, Project, ProjectSchema
from sqlalchemy_searchable import search

app = Flask(__name__)
app.config.from_object("config")

UPLOAD_FOLDER = '/home/george/Documents/vgg-docs/vgg-project-challenge/app/uploads'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

PROJECTS_SCHEMA = ProjectSchema(many=True)
PROJECT_SCHEMA = ProjectSchema()

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

class ProjectResource(Resource):

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    """
    Get all projects in the database
    """
    def get(self, project_id=None):
        if project_id is not None:
            project = Project.query.filter_by(id=project_id).all()
            project = PROJECTS_SCHEMA.dump(project).data
            return {'status': 'success', 'data': project}, 200
        elif request.args.get('search') is not None:
            term = request.args.get('search')
            projects = Project.query.filter((Project.name.ilike('%' + term + '%')) | (Project.description.ilike('%' + term + '%'))).all()
            if projects:
                projects = PROJECTS_SCHEMA.dump(projects).data
                return {"status": 'success', "data": projects}, 200
            else:
                return {"status": "Resource not found"}, 404
        elif request.args.get('offset') is not None and request.args.get('limit') is not None:
            if int(request.args.get('offset')) >= 0 or int(request.args.get('limit')) > 0:
                limit = request.args.get('limit')
                offset = request.args.get('offset')
                projects = Project.query.offset(offset).limit(limit)
                if projects:
                    projects = PROJECTS_SCHEMA.dump(projects).data
                    return {"status": "success", 'data': projects}, 200
                else:
                    return {"status": 'Resource not found'}, 404
            else:
                return {"status":"Error", "message": "Offet value must greater or equal to zero and limit value must be greater than 0"}, 500
        elif request.args.get('offset') is not None or request.args.get('limit') is not None:
            if request.args.get('offset') is not None and int(request.args.get('offset')) >= 0:
                offset = request.args.get('offset')
                projects = Project.query.offset(offset)
                if projects:
                    projects = PROJECTS_SCHEMA.dump(projects).data
                    return {"statue": "success", "data": projects}, 200
                else:
                    return {"status": "Resource not found"}, 404
            elif request.args.get('limit') is not None and int(request.args.get('limit')) > 0:
                limit = request.args.get('limit')
                projects = Project.query.limit(limit)
                if projects:
                    projects = PROJECTS_SCHEMA.dump(projects).data
                    return {"status": "success", "data": projects}, 200
                else:
                    return {"status": "Resource not found"}, 404
        elif project_id == None:
            projects = Project.query.all()
            projects = PROJECTS_SCHEMA.dump(projects).data
            return {'status': 'success', 'data': projects}, 200
        else:
            return {"status": "Resource not found"}, 404

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
            completed=json_data['completed'],
            user_stories=""
        )
        db.session.add(project)
        db.session.commit()

        result = PROJECT_SCHEMA.dump(project).data
        return {
            "status": 'success',
            "data": result
        }, 201

    def put(self, project_id=None):
        # check if the post request has the file part
        if 'file' not in request.files:
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
            return {'status': 'success', 'data': result}, 200
        else:
            # check if tha projectid exists
            if project_id == None:
                return {"status": "Resource does not exist!"}, 404
            else:
                finfo = request
                # check if the post request has the file part
                file = request.files['file']
                if file.filename == '':
                    return {'message' : 'No file selected for uploading'}, 500
                if file and self.allowed_file(file.filename):
                    # put file url in projects database
                    project = Project.query.filter_by(id=project_id).first()
                    if project:
                        filename = secure_filename(file.filename)
                        project.user_stories = str(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        db.session.commit()
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        return {'message' : 'File successfully uploaded'}, 200
                    else:
                        return {"status": "Resource no found"}, 404
                else:
                    return {'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'}, 400
                    



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


