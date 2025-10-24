from app import db 

class ONG(db.Model):
    __tablename__ = "ongs"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128))

    # Relación a los proyectos de la ONG
    projects = db.relationship('ProjectDefinition', back_populates='creador_ong')
    # Relación a los compromisos de la ONG
    compromisos = db.relationship('Compromiso', back_populates='compromiso_ong')