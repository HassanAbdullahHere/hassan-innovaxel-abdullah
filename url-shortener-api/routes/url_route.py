from flask import Blueprint, request, jsonify
from utils.shortener import generate_short_code
from models.url_model import increment_access, insert_url, find_by_short_code
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

    # Optionally increment access count
    increment_access(short_code)

    return jsonify({
        "id": str(doc.get('_id')),
        "url": doc.get('url'),
        "shortCode": doc.get('shortCode'),
        "createdAt": doc.get('createdAt'),
        "updatedAt": doc.get('updatedAt')
    }), 200
