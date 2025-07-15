from flask import Blueprint, request, jsonify
from utils.shortener import generate_short_code
from models.url_model import insert_url, find_by_short_code
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
