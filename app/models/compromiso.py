from app import db

class Compromiso(db.Model):
    __tablename__ = "compromisos"

    id = db.Column(db.Integer, primary_key=True)
    
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedidos_colaboracion.id"), nullable=False)
    ong_id = db.Column(db.Integer, db.ForeignKey("ongs.id"), nullable=False) # La ONG que ayuda
    
    details = db.Column(db.Text) # "Yo puedo cubrir 500 USD"
    amount_committed = db.Column(db.Float, default=0)
    status = db.Column(db.String(50), default='pending') # 'pending', 'fulfilled'

    pedido = db.relationship("PedidoColaboracion", back_populates="compromisos")
    compromiso_ong = db.relationship("ONG", back_populates="compromisos")