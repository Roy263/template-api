from pymongo import MongoClient
import hashlib
import json
import datetime
from flask_jwt_extended import create_access_token

# Load the MongoDB URI from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

mongodb_uri = config['MONGODB_URI']
db_name=config['DATABASE_NAME']

# Create a MongoClient using the loaded MongoDB URI
client = MongoClient(mongodb_uri)
db = client[db_name]
users_collection = db['Users']

def registerUser(data):
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    password = data['password']

    existing_user = users_collection.find_one({'email': email})

    if existing_user:
        return {'error': 'User with this email already exists'}, 400

    # Hash the password using SHA-256 before storing it
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    # Create a new user document and insert it into the database
    new_user = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password_hash  # Store the hashed password
    }

    users_collection.insert_one(new_user)

    return {'message': 'User registered successfully'}, 201

def loginUser(data):
    email = data['email']
    password = data['password']

    # Check if the email and password match a user in the database
    user = users_collection.find_one({'email': email, 'password': hashlib.sha256(password.encode()).hexdigest()})

    if not user:
        return {'error': 'Invalid credentials'}, 401
    
    expires = datetime.timedelta(hours=1)

    # If the credentials are valid, create an access token and return it
    access_token = create_access_token(identity=email,expires_delta=expires)
    return {'access_token': access_token}, 200

