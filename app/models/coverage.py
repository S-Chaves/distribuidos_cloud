from app import db 
from datetime import datetime

class CoveragePlan(db.Model):
    __tablename__ = "coverage_plans"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project_definitions.id"), nullable=False)
    strategy = db.Column(db.Text)
    organizations = db.Column(db.ARRAY(db.String))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)

    project = db.relationship("ProjectDefinition", back_populates="coverage_plan")
    pedidos = db.relationship("PedidoColaboracion", back_populates="coverage_plan")