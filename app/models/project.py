from app import db 
from datetime import datetime

class ProjectDefinition(db.Model):
    __tablename__ = "project_definitions"

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(255), nullable=False)
    ong_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    country = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    project_types = db.Column(db.ARRAY(db.String), nullable=True)
    budget = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    objectives = db.Column(db.Text, nullable=False)
    beneficiaries = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    creador_ong_id = db.Column(db.Integer, db.ForeignKey("ongs.id"), nullable=False)
    creador_ong = db.relationship("ONG", back_populates="projects")

    coverage_plan = db.relationship("CoveragePlan", back_populates="project", uselist=False)
    work_plan = db.relationship("WorkPlan", back_populates="project", uselist=False)