from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from controllers.user_controller import registerUser,loginUser
from controllers.template_controller import create_template,get_all_templates,get_template_by_id,update_template_by_id,delete_template_by_id
import json

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = config['JWT_SECRET_KEY']
jwt = JWTManager(app)

# Hello path
@app.route('/')
def hello():
    return jsonify({"message":"Hello World!"}),200

# User registration
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    result, status_code = registerUser(data)
    return jsonify(result), status_code

# User login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    result, status_code = loginUser(data)
    return jsonify(result), status_code

# Create New Template
@app.route('/template', methods=['POST'])
@jwt_required()
def createTemplate():
    try:
        current_user = get_jwt_identity()  # This line should be inside the try block
        data = request.get_json()
        data['user_email'] = current_user
        result, status_code = create_template(data) 
        return result, status_code
    except Exception as e:
        return jsonify({'error': 'Failed to create template'}), 500


@app.route('/template', methods=['GET'])
@jwt_required()
def get_templates():
    try:
        # Retrieve all templates from the database
        result,status_code=get_all_templates()
        return result, status_code
    except Exception as e:
        return jsonify({'error': 'Failed to get templates'}), 500
    
@app.route('/template/<template_id>', methods=['GET'])
@jwt_required()
def get_template(template_id):
    try:
        # Retrieve the template from the database
        result,status_code=get_template_by_id(template_id)
        return result, status_code
    except Exception as e:
        return jsonify({'error': 'Failed to get templates'}), 500

@app.route('/template/<template_id>', methods=['PUT'])
@jwt_required()
def update_template(template_id):
    data = request.get_json()
    try:
        # Update the template with the given ID in the database
        result,status_code=update_template_by_id(template_id,data)
        return result, status_code
    except Exception as e:
        return jsonify({'error': 'Failed to get templates'}), 500
   
@app.route('/template/<template_id>', methods=['DELETE'])
@jwt_required()
def delete_template(template_id):
    try:
        # Delete the template with the given ID from the database
        result,status_code=delete_template_by_id(template_id)
        return result, status_code
    except Exception as e:
        return jsonify({'error': 'Failed to get templates'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001,debug=True)
