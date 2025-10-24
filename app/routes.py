from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import db

from .models import ONG, ProjectDefinition, WorkPlan, CoveragePlan, PedidoColaboracion, Compromiso

api = Blueprint('api', __name__)

@api.route('/pedidos', methods=['GET'])
@jwt_required()
def get_pedidos():
    """
    Visualización de todos los pedidos de colaboración que están 'abiertos'.
    Cualquier ONG autenticada puede ver esta lista.
    ---
    tags:
      - Pedidos y Compromisos
    security:
      - bearerAuth: []
    responses:
      200:
        description: Una lista de todos los pedidos de colaboración abiertos.
        schema:
          type: array
          items:
            properties:
              id: { type: integer }
              request_type: { type: string }
              description: { type: string }
              amount_requested: { type: number }
              project_name: { type: string }
              project_country: { type: string }
              creador_ong_name: { type: string }
    """
    # Buscamos todos los pedidos que no estén 'covered'
    open_pedidos = PedidoColaboracion.query.filter(PedidoColaboracion.status != 'covered').all()
    
    results = []
    for p in open_pedidos:
        results.append({
            "id": p.id,
            "request_type": p.request_type,
            "description": p.description,
            "amount_requested": p.amount_requested,
            "project_name": p.coverage_plan.project.project_name,
            "project_country": p.coverage_plan.project.country,
            "creador_ong_name": p.coverage_plan.project.creador_ong.name
        })
        
    return jsonify(results)

@api.route('/pedidos/<int:pedido_id>/comprometerse', methods=['POST'])
@jwt_required()
def make_commitment(pedido_id):
    """
    Permite a una ONG (que NO es dueña del proyecto) crear un compromiso 
    para ayudar con un pedido específico.
    ---
    tags:
      - Pedidos y Compromisos
    security:
      - bearerAuth: []
    parameters:
      - in: path
        name: pedido_id
        description: "El ID del pedido al que se quiere ayudar."
        required: true
        schema: { type: integer }
      - in: body
        name: body
        required: true
        schema:
          properties:
            details:
              type: string
              example: "Puedo donar 50 bolsas de cemento la próxima semana."
            amount_committed:
              type: number
              example: 50
    responses:
      201:
        description: Compromiso creado exitosamente.
      403:
        description: No puedes comprometerte a un pedido de tu propio proyecto.
      404:
        description: Pedido no encontrado o ya está cubierto.
    """
    current_ong_id = int(get_jwt_identity())
    
    # Buscamos el pedido
    pedido = PedidoColaboracion.query.get(pedido_id)

    if not pedido or pedido.status != 'open':
        return jsonify({"msg": "Pedido no encontrado o ya está cubierto"}), 404
        
    # Verificamos que la ONG que ayuda no sea la misma que creó el proyecto
    if pedido.coverage_plan.project.creador_ong_id == current_ong_id:
        return jsonify({"msg": "No puedes comprometerte a un pedido de tu propio proyecto"}), 403

    data = request.get_json()
    if not data or 'details' not in data or 'amount_committed' not in data:
        return jsonify({"msg": "Faltan los campos 'details' y 'amount_committed'"}), 400

    new_compromiso = Compromiso(
        pedido_id=pedido.id,
        ong_id=current_ong_id,
        details=data.get('details'),
        amount_committed=data.get('amount_committed'),
        status='pending' # El compromiso inicia como 'pendiente'
    )
    db.session.add(new_compromiso)
    db.session.commit()
    
    return jsonify({
        "msg": "Compromiso creado exitosamente", 
        "compromiso_id": new_compromiso.id
    }), 201

@api.route('/compromisos/<int:compromiso_id>/cumplido', methods=['PUT'])
@jwt_required()
def fulfill_commitment(compromiso_id):
    """
    Marca un compromiso como 'cumplido' (fulfilled).
    Solo la ONG dueña del proyecto puede marcar un compromiso como cumplido.
    ---
    tags:
      - Pedidos y Compromisos
    security:
      - bearerAuth: []
    parameters:
      - in: path
        name: compromiso_id
        description: "El ID del compromiso a marcar como cumplido."
        required: true
        schema: { type: integer }
    responses:
      200:
        description: Compromiso marcado como 'cumplido'.
      403:
        description: No tienes permiso para aprobar este compromiso (solo el dueño del proyecto puede).
      404:
        description: Compromiso no encontrado.
    """
    current_ong_id = int(get_jwt_identity())
    
    # Buscamos el compromiso
    compromiso = Compromiso.query.get(compromiso_id)
    
    if not compromiso:
        return jsonify({"msg": "Compromiso no encontrado"}), 404
    
    # Verificación de Permiso: 
    # El ID del usuario (token) debe ser igual al ID del creador del proyecto
    project_owner_id = compromiso.pedido.coverage_plan.project.creador_ong_id
    if project_owner_id != current_ong_id:
        return jsonify({"msg": "No tienes permiso para aprobar este compromiso"}), 403

    # Actualizamos el estado
    compromiso.status = 'fulfilled'
    db.session.add(compromiso)
    
    db.session.commit()
    
    return jsonify({"msg": "Compromiso marcado como 'cumplido'"})

@api.route('/proyectos/<int:project_id>/pedidos', methods=['GET'])
@jwt_required()
def get_project_pedidos(project_id):
    """
    Obtiene todos los pedidos (abiertos y cubiertos) de un proyecto específico.
    Cualquier ONG autenticada puede ver esta lista.
    ---
    tags:
      - Proyectos
    security:
      - bearerAuth: []
    parameters:
      - in: path
        name: project_id
        description: "El ID del proyecto que se quiere consultar."
        required: true
        schema: { type: integer }
    responses:
      200:
        description: Una lista de todos los pedidos para el proyecto.
        schema:
          type: array
          items:
            properties:
              id: { type: integer }
              request_type: { type: string }
              description: { type: string }
              amount_requested: { type: number }
              status: { type: string }
      404:
        description: Proyecto no encontrado.
    """
    project = ProjectDefinition.query.get(project_id)
    if not project:
        return jsonify({"msg": "Proyecto no encontrado"}), 404
        
    # Accedemos a los pedidos a través del plan de cobertura
    pedidos = project.coverage_plan.pedidos
    
    results = [
        {
            "id": p.id,
            "request_type": p.request_type,
            "description": p.description,
            "amount_requested": p.amount_requested,
            "status": p.status
        } for p in pedidos
    ]
    
    return jsonify(results)

@api.route('/proyectos/<int:project_id>/compromisos', methods=['GET'])
@jwt_required()
def get_project_compromisos(project_id):
    """
    Obtiene todos los compromisos (pendientes y cumplidos) de un proyecto.
    Solo la ONG dueña del proyecto puede ver esta lista.
    ---
    tags:
      - Proyectos
    security:
      - bearerAuth: []
    parameters:
      - in: path
        name: project_id
        description: "El ID del proyecto para ver sus compromisos."
        required: true
        schema: { type: integer }
    responses:
      200:
        description: Una lista de todos los compromisos para el proyecto.
      403:
        description: No estás autorizado para ver esta información.
      404:
        description: Proyecto no encontrado.
    """
    current_ong_id = int(get_jwt_identity())
    project = ProjectDefinition.query.get(project_id)
    
    if not project:
        return jsonify({"msg": "Proyecto no encontrado"}), 404
        
    # Verificación de autorización (usando la navegación simple)
    if project.creador_ong_id != current_ong_id:
        return jsonify({"msg": "No estás autorizado para ver los compromisos de este proyecto"}), 403

    results = []
    
    # 1. Navegamos al plan de cobertura
    if not project.coverage_plan:
        return jsonify(results) # No hay plan, no hay compromisos

    # 2. Navegamos a los pedidos de ese plan
    pedidos_del_proyecto = project.coverage_plan.pedidos
    
    # 3. Recorremos los pedidos y luego sus compromisos
    for p in pedidos_del_proyecto:
        for comp in p.compromisos:
            results.append({
                "compromiso_id": comp.id,
                "compromiso_status": comp.status,
                "details": comp.details,
                "amount_committed": comp.amount_committed,
                "pedido_id": p.id,
                "pedido_description": p.description,
                "compromiso_ong_name": comp.compromiso_ong.name 
            })
        
    return jsonify(results)