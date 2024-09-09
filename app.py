from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# In-memory storage for passwords with UUIDs
passwords = []

# Route to save a new password with a provided UUID
@app.route('/api/save_password', methods=['POST'])
def save_password():
    data = request.json
    if 'password' not in data or 'uuid' not in data:
        return jsonify({'error': 'UUID and password are required'}), 400

    # Check if an entry with the same UUID already exists
    for entry in passwords:
        if entry['uuid'] == data['uuid']:
            # Update the password and return a message
            entry['password'] = data['password']
            entry['created_at'] = datetime.utcnow()
            return jsonify({'message': 'Password updated successfully'}), 200

    # If no existing entry, create a new one
    new_password = {
        'uuid': data['uuid'],
        'password': data['password'],
        'created_at': datetime.utcnow()
    }
    passwords.append(new_password)

    return jsonify({'message': 'Password saved successfully'}), 201

# Route to get passwords by UUID
@app.route('/api/get_passwords', methods=['GET'])
def get_passwords():
    uuid_param = request.args.get('uuid')
    if not uuid_param:
        return jsonify({'error': 'UUID is required'}), 400

    # Find the password associated with the given UUID
    user_password = next((p for p in passwords if p['uuid'] == uuid_param), None)

    if not user_password:
        return jsonify({'message': 'No password found for the provided UUID'}), 404

    return jsonify(user_password)

if __name__ == '__main__':
    app.run()
