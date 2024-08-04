from flask import Blueprint, request, jsonify
import asyncio
import logging

# Import functions from generator.py
from src.rag.generator.generator import ask_general_advisory, generate_specific_advisory

# Create a Blueprint
api_bp = Blueprint('api', __name__)

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@api_bp.route('/advisory/general', methods=['POST'])
def general_advisory():
    """Endpoint for general financial advisory questions."""
    try:
        data = request.json  # Get JSON data from request
        question = data.get('question')

        if not question:
            return jsonify({'error': 'Question is required'}), 400

        # Use asyncio.run() to call async function
        response = asyncio.run(ask_general_advisory(question))

        return jsonify({'response': response}), 200

    except Exception as e:
        logging.error(f"Error in general advisory: {e}")
        return jsonify({'error': 'Something went wrong'}), 500

@api_bp.route('/advisory/specific', methods=['POST'])
def specific_advisory():
    """Endpoint for specific financial advisory with user data."""
    try:
        data = request.json  # Get JSON data from request
        user_id = data.get('user_id')
        question = data.get('question')

        if not user_id or not question:
            return jsonify({'error': 'User ID and question are required'}), 400

        # Use asyncio.run() to call async function
        response = asyncio.run(generate_specific_advisory(user_id, question))

        return jsonify({'response': response}), 200

    except Exception as e:
        logging.error(f"Error in specific advisory: {e}")
        return jsonify({'error': 'Something went wrong'}), 500
