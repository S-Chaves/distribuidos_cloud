# app/models.py
from . import db # Assuming 'db' is your SQLAlchemy instance

class ONG(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128))

# class Project(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(150), nullable=False)
#     originating_ngo_id = db.Column(db.Integer, db.ForeignKey('ngo.id'))
#     # ... other project details

# class CollaborationRequest(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
#     request_type = db.Column(db.String(50)) # e.g., 'dinero', 'materiales', 'mano de obra' [cite: 24]
#     details = db.Column(db.Text, nullable=False)
#     status = db.Column(db.String(50), default='open') # open, covered

# class Commitment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     request_id = db.Column(db.Integer, db.ForeignKey('collaboration_request.id'), nullable=False)
#     committing_ngo_id = db.Column(db.Integer, db.ForeignKey('ngo.id'), nullable=False)
#     details = db.Column(db.Text)
#     status = db.Column(db.String(50), default='pending') # pending, fulfilled