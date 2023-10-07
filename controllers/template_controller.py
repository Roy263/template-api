from flask_jwt_extended import get_jwt_identity
from pymongo import MongoClient
from bson import ObjectId
import json

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

mongodb_uri = config['MONGODB_URI']
db_name=config['DATABASE_NAME']

# Create a MongoClient using the loaded MongoDB URI
client = MongoClient(mongodb_uri)
db = client[db_name]
users_collection = db['Users']
templates_collection = db['templates']

def create_template(data):
    print(data)
    try:
        # Insert the new template into the database
        result = templates_collection.insert_one(data)

        if result.inserted_id:
            return {'message': 'Template created successfully'}, 201
        else:
            return {'error': 'Failed to create template'}, 400
    except Exception as e:
        return {'error': str(e)}, 500

def get_all_templates():
    try:
        # Retrieve all templates from the database
        templates = list(templates_collection.find({}))

        # Prepare the response as a list of templates
        template_list = [{'template_name': template['template_name'], 'subject': template['subject'], 'body': template['body']} for template in templates]

        return {'templates': template_list}, 200
    except Exception as e:
        return {'error': str(e)}, 500
    
def get_template_by_id(template_id):
    try:
        # Retrieve a single template by its ID from the database
        template = templates_collection.find_one({'_id': ObjectId(template_id)})

        if template:
            # Prepare the response for the found template
            template_data = {
                'template_name': template['template_name'],
                'subject': template['subject'],
                'body': template['body']
            }
            return {'template': template_data}, 200
        else:
            return {'error': 'Template not found'}, 404
    except Exception as e:
        return {'error': str(e)}, 500
    
def update_template_by_id(template_id, updated_data):
    try:
        # Update the template with the given ID in the database
        result = templates_collection.update_one(
            {'_id': ObjectId(template_id)},
            {'$set': updated_data}
        )

        if result.modified_count > 0:
            return {'message': 'Template updated successfully'}, 200
        else:
            return {'error': 'Template not found or not updated'}, 404
    except Exception as e:
        return {'error': str(e)}, 500
    
def delete_template_by_id(template_id):
    try:
        # Delete the template with the given ID from the database
        result = templates_collection.delete_one({'_id': ObjectId(template_id)})

        if result.deleted_count > 0:
            return {'message': 'Template deleted successfully'}, 200
        else:
            return {'error': 'Template not found or not deleted'}, 404
    except Exception as e:
        return {'error': str(e)}, 500