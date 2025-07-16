from flask import Blueprint, request, jsonify
from utils.shortener import generate_short_code
from models.url_model import delete_url, increment_access, insert_url, find_by_short_code, update_url
from datetime import datetime

url_blueprint = Blueprint("url_routes", __name__)

@url_blueprint.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')

    if not original_url:
        return jsonify({"error": "URL is required"}), 400

    short_code = generate_short_code()
    existing = find_by_short_code(short_code)

    while existing:
        short_code = generate_short_code()
        existing = find_by_short_code(short_code)

    inserted_id = insert_url(original_url, short_code)

    now = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

    return jsonify({
        "id": str(inserted_id),
        "url": original_url,
        "shortCode": short_code,
        "createdAt": now,
        "updatedAt": now
    }), 201
    
@url_blueprint.route('/shorten/<short_code>', methods=['GET'])
def get_original_url(short_code):
    doc = find_by_short_code(short_code)

    if not doc:
        return jsonify({"error": "Short URL not found"}), 404

    increment_access(short_code)

    return jsonify({
        "id": str(doc.get('_id')),
        "url": doc.get('url'),
        "shortCode": doc.get('shortCode'),
        "createdAt": doc.get('createdAt'),
        "updatedAt": doc.get('updatedAt')
    }), 200
    
@url_blueprint.route('/shorten/<short_code>/stats', methods=['GET'])
def get_url_stats(short_code):
    doc = find_by_short_code(short_code)

    if not doc:
        return jsonify({"error": "Short URL not found"}), 404

    return jsonify({
        "id": str(doc.get('_id')),
        "url": doc.get('url'),
        "shortCode": doc.get('shortCode'),
        "createdAt": doc.get('createdAt'),
        "updatedAt": doc.get('updatedAt'),
        "accessCount": doc.get('accessCount', 0)
    }), 200

@url_blueprint.route('/shorten/<short_code>', methods=['PUT'])
def update_short_url(short_code):
    data = request.get_json()
    new_url = data.get('url')

    if not new_url:
        return jsonify({"error": "URL is required"}), 400

    updated_doc = update_url(short_code, new_url)

    if not updated_doc:
        return jsonify({"error": "Short URL not found"}), 404

    return jsonify({
        "id": str(updated_doc.get('_id')),
        "url": updated_doc.get('url'),
        "shortCode": updated_doc.get('shortCode'),
        "createdAt": updated_doc.get('createdAt'),
        "updatedAt": updated_doc.get('updatedAt')
    }), 200
    
@url_blueprint.route('/shorten/<short_code>', methods=['DELETE'])
def delete_short_url(short_code):
    success = delete_url(short_code)

    if not success:
        return jsonify({"error": "Short URL not found"}), 404

    return '', 204
