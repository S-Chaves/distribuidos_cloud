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
    
    # Limpiamos todo para empezar de cero
    db.drop_all()
    db.create_all()
    
    try:
        # 1. Crear ONGs de prueba
        hashed_pass_1 = generate_password_hash('pass123', method='pbkdf2:sha256')
        hashed_pass_2 = generate_password_hash('pass456', method='pbkdf2:sha256')
        
        ong_creadora = ONG(name="ONG-Creadora-Test", password=hashed_pass_1)
        ong_colaboradora = ONG(name="ONG-Colaboradora-Test", password=hashed_pass_2)
        
        db.session.add(ong_creadora)
        db.session.add(ong_colaboradora)
        db.session.commit() # Guardamos para obtener los IDs

        # 2. Crear un Proyecto de prueba (vinculado a la ONG Creadora)
        # Usamos todos los campos que definiste en tu modelo
        proyecto = ProjectDefinition(
            creador_ong_id=ong_creadora.id,
            project_name="Proyecto de Agua Potable - Test",
            ong_name="ONG-Creadora-Test",
            description="Instalación de sistema de purificación en comunidad.",
            country="Argentina",
            location="Provincia de Buenos Aires",
            project_types=["Agua", "Infraestructura"],
            budget=50000.0,
            duration=6, # 6 meses
            objectives="Proveer agua limpia a 100 familias.",
            beneficiaries="Comunidad local de 300 personas.",
            created_at=datetime.now()
        )
        db.session.add(proyecto)
        db.session.commit() # Guardamos para obtener el ID

        # 3. Crear el Plan de Trabajo y Cobertura (vinculados al Proyecto)
        work_plan = WorkPlan(
            project_id=proyecto.id,
            stages=[{"name": "Etapa 1: Relevamiento", "start": "2025-11-01", "end": "2025-11-15"}],
            monitoring_plan="Seguimiento semanal."
        )
        
        coverage_plan = CoveragePlan(
            project_id=proyecto.id,
            strategy="Buscar donaciones de materiales y fondos."
        )
        db.session.add(work_plan)
        db.session.add(coverage_plan)
        db.session.commit() # Guardamos para obtener el ID

        # 4. Crear los Pedidos de Colaboración (vinculados al Plan de Cobertura)
        pedido_1 = PedidoColaboracion(
            coverage_plan_id=coverage_plan.id,
            request_type="materiales",
            description="100 bolsas de cemento",
            amount_requested=100,
            status='open'
        )
        
        pedido_2 = PedidoColaboracion(
            coverage_plan_id=coverage_plan.id,
            request_type="dinero",
            description="Fondos para transporte",
            amount_requested=2500.0,
            status='open'
        )
        
        pedido_3 = PedidoColaboracion(
            coverage_plan_id=coverage_plan.id,
            request_type="mano de obra",
            description="Voluntarios para construcción",
            amount_requested=10, # 10 personas
            status='covered' # Este ya está cubierto (no debe aparecer en la API)
        )
        
        db.session.add_all([pedido_1, pedido_2, pedido_3])
        db.session.commit()
        
        print("-----------------------------------------")
        print("¡Base de datos sembrada con éxito!")
        print("\nUsuarios de prueba:")
        print(f"  ONG Creadora:     name='{ong_creadora.name}', password='pass123'")
        print(f"  ONG Colaboradora: name='{ong_colaboradora.name}', password='pass456'")
        print("\nPedidos abiertos creados: 2")
        print("-----------------------------------------")

    except Exception as e:
        db.session.rollback()
        print(f"Error al sembrar la base de datos: {e}")
