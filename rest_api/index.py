import json
from flask import Blueprint, request, jsonify

# main blueprint
api = Blueprint('api', __name__, url_prefix='/api')


# data storage
FILE_PATH = "data\data.json"



# GET users
# Fetch users
@api.route('/users', methods=['GET'])
def get_users():
    # get file size
    with open(FILE_PATH, 'r') as f:
        inital = f.tell()
        f.seek(0, 2)
        size = f.tell() - inital
        if size >= 2:
            f.seek(0, 0)
            data = json.load(f)
            return jsonify(data)
        else:
            return jsonify([])




# GET user/1
# Fetch 1 user
@api.route('/user/<int:id>', methods=['GET'])
def get_one_user(id: int):
    with open(FILE_PATH, 'r') as f:
        inital = f.tell()
        f.seek(0, 2)
        size = f.tell() - inital
        if size >= 2:
            f.seek(0, 0)
            data = json.load(f)  
        else:
            return jsonify({'message':'user not found'})
    index = None
    for idx, user in enumerate(data):
        if user['id'] == id:
            index = idx
    if index is not None:
        return jsonify(data[index])
    else:
        return jsonify({'message':'user not found'})




# POST /users
# Create 1 user
@api.route('/users', methods=['POST'])
def post_users():
    # get json payload
    post_data = json.loads(request.data)
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        inital = f.tell()
        f.seek(0, 2)
        size = f.tell() - inital
        if size >= 2:
            f.seek(0, 0)
            data = json.load(f)  
        else:
            data = []
    data.append(post_data)
    # write new list to file
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, sort_keys=True)
    return {'message':'user created'}




# PATCH /user/1
# Update 1 user
@api.route('/user/<int:id>', methods=['PATCH'])
def update_one_user(id: int):
    # search user
    with open(FILE_PATH, 'r') as f:
        inital = f.tell()
        f.seek(0, 2)
        size = f.tell() - inital
        if size >= 2:
            f.seek(0, 0)
            data = json.load(f)  
        else:
            return jsonify({'message':'user not found'})
    index = None
    for idx, user in enumerate(data):
        if user['id'] == id:
            index = idx
    # user found
    if index is not None:
        updated_data = json.loads(request.data)
        data[index]['name'] = updated_data['name']
        # write updated data to file
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, sort_keys=True)
            return jsonify({'message':'user updated'})
    # user not found
    else:
        return jsonify({'message':'user not found'})




# DELETE /user/1
# Delete 1 user
@api.route('/user/<int:id>', methods=['DELETE'])
def delete_one_user(id: int):
    with open(FILE_PATH, 'r') as f:
        inital = f.tell()
        f.seek(0, 2) # file cursor to end of file
        size = f.tell() - inital
        if size >= 2:
            f.seek(0, 0) # file cursor to start of file
            data = json.load(f)  
        else:
            return jsonify({'message':'user not found'})
    index = None
    for idx, user in enumerate(data):
        if user['id'] == id:
            index = idx
    if index is not None:
        data.pop(index)
        # write updated data
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, sort_keys=True)
        return jsonify({'message':'user deleted'})
    else:
        return jsonify({'message':'user not found'})