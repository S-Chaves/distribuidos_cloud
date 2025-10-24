from app import db

class PedidoColaboracion(db.Model):
    __tablename__ = "pedidos_colaboracion"
    
    id = db.Column(db.Integer, primary_key=True)
    
    request_type = db.Column(db.String(50), nullable=False) # 'económica', 'materiales', 'mano de obra', "equipamiento", "asesoramiento tecnico"
    description = db.Column(db.Text, nullable=False)
    amount_requested = db.Column(db.Float, default=0)
    status = db.Column(db.String(50), default='open') # 'open', 'covered'

    compromisos = db.relationship("Compromiso", back_populates="pedido")
    coverage_plan_id = db.Column(db.Integer, db.ForeignKey("coverage_plans.id"), nullable=False)
    coverage_plan = db.relationship("CoveragePlan", back_populates="pedidos")