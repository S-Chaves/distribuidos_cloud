from app import db 
from datetime import datetime

class WorkPlan(db.Model):
    __tablename__ = "work_plans"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project_definitions.id"), nullable=False)
    stages = db.Column(db.JSON, nullable=False)  # [{name, start, end, activities, resources}]
    monitoring_plan = db.Column(db.Text)
    risk_analysis = db.Column(db.Text)
    success_indicators = db.Column(db.Text)
    terms_accepted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    project = db.relationship("ProjectDefinition", back_populates="work_plan")
