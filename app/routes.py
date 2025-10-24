# app/routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
# from .models import CollaborationRequest, Commitment, NGO
from . import db

api = Blueprint('api', __name__)

# @api.route('/requests', methods=['GET'])
# @jwt_required()
# def get_collaboration_requests():
#     """
#     View all open collaboration requests
#     ---
#     tags:
#       - Requests
#     security:
#       - bearerAuth: []
#     responses:
#       200:
#         description: A list of open collaboration requests.
#     """
    
#     # Query the database for all requests with 'open' status
#     open_requests = CollaborationRequest.query.filter_by(status='open').all()
    
#     # Format the data for the JSON response
#     results = [
#         {
#             "id": req.id,
#             "project_id": req.project_id,
#             "request_type": req.request_type,
#             "details": req.details,
#             "status": req.status
#         } for req in open_requests
#     ]
    
#     return jsonify(results)

# @api.route('/requests/<int:request_id>/commit', methods=['POST'])
# @jwt_required()
# def make_commitment(request_id):
#     """Endpoint for an NGO to commit to a request."""
#     # Logic to create a new Commitment in the database
#     current_ngo_id = get_jwt_identity()
#     return jsonify({"message": f"Commitment made to request {request_id} by NGO {current_ngo_id}"})

# @api.route('/commitments/<int:commitment_id>/fulfill', methods=['PATCH'])
# @jwt_required()
# def fulfill_commitment(commitment_id):
#     """Endpoint to mark a commitment as fulfilled."""
#     # Logic to update the status of a specific Commitment
#     return jsonify({"message": f"Commitment {commitment_id} marked as fulfilled"})