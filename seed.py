import click
from flask.cli import with_appcontext
from app import db
from app.models import ONG, ProjectDefinition, WorkPlan, CoveragePlan, PedidoColaboracion, Compromiso
from werkzeug.security import generate_password_hash
from datetime import datetime

@click.command('seed-db')
@with_appcontext
def seed_db_command():
    """Crea datos de ejemplo en la base de datos para pruebas."""
    
    # Comprobamos si los datos ya existen para no duplicar.
    try:
        # 1. Comprobar si la ONG creadora ya existe
        ong_creadora = ONG.query.filter_by(name="ong_originante").first()
        if not ong_creadora:
            print("Creando ONG Creadora de prueba...")
            hashed_pass_1 = generate_password_hash('pass123', method='pbkdf2:sha256')
            ong_creadora = ONG(name="ong_originante", password=hashed_pass_1)
            db.session.add(ong_creadora)

        # 2. Comprobar si la ONG colaboradora ya existe
        ong_colaboradora = ONG.query.filter_by(name="ong_red").first()
        if not ong_colaboradora:
            print("Creando ONG Colaboradora de prueba...")
            hashed_pass_2 = generate_password_hash('pass456', method='pbkdf2:sha256')
            ong_colaboradora = ONG(name="ong_red", password=hashed_pass_2)
            db.session.add(ong_colaboradora)
            
            
            print("-----------------------------------------")
            print("¡Base de datos sembrada con éxito!")
            print("\nUsuarios de prueba:")
            print(f"  ONG Creadora:    name='{ong_creadora.name}', password='pass123'")
            print(f"  ONG Colaboradora: name='{ong_colaboradora.name}', password='pass456'")
            print("-----------------------------------------")
        
        else:
            print("La base de datos ya contenía datos de prueba. No se ha modificado nada.")

    except Exception as e:
        db.session.rollback()
        print(f"Error al sembrar la base de datos: {e}")