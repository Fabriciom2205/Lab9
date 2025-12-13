from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

token_storage = {}

@app.route('/create-token', methods=['POST'])
def create_token():

    data = request.get_json()
    user_id = data.get('id')
    
    if not user_id:
        return jsonify({"error": "No user ID provided"}), 400

    new_token = str(uuid.uuid4())
    
    token_storage[new_token] = user_id
    
    return jsonify({
        "id": user_id,
        "uuid-token": new_token,
        "message": "Token created successfully"
    }), 201

@app.route('/verify-token', methods=['POST'])
def verify_token():
    data = request.get_json()
    token = data.get('uuid-token')
    
    if not token:
        return jsonify({"error": "No token provided"}), 400
    
    if token in token_storage:
        return jsonify({
            "valid": True,
            "id": token_storage[token],
            "message": "Token is valid"
        }), 200
    else:
        return jsonify({
            "valid": False,
            "message": "Token is invalid or expired"
        }), 401

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "Server is running!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)