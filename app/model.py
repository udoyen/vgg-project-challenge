from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

ma = Marshmallow()
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    completed = db.Column(db.Boolean, nullable=True)
    user_stories = db.Column(db.String, nullable=True, server_default="")

    def __init__(self, name, description, completed, user_stories):
        self.name = name
        self.description = description
        self.completed = completed
        self.user_stories = user_stories

class Action(db.Model):
    __tablename__ = 'actions'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(250), nullable=False)
    note = db.Column(db.String(500), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, project_id, description, note):
        self.project_id = project_id
        self.description = description
        self.note = note

# Schema validations
class UserSchema(ma.Schema):
    id = fields.Integer()
    username = fields.String(required=True)
    password = fields.String(required=True)

class ProjectSchema(ma.Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    description = fields.String(required=False)
    completed = fields.Boolean(required=True)
    user_stories = fields.String(required=False)

class ActionSchema(ma.Schema):
    id = fields.Integer()
    project_id = fields.Integer(required=True)
    description = fields.String(required=True)
    note = fields.String(required=True)
