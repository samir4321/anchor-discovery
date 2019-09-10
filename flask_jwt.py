from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)

USERS = ['bob', 'alice', 'admin']

ADMIN_DATABASE = {
    'bob': 'came in last thursday',
    'alice': "hasn't been seen in a while",
}

USER_DATABASE = {
    'bob': 'bobs stuff',
    'alice': 'alices stuff'
}

# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token, and you can return
# it to the caller however you choose.
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if username == 'admin':
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200

    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if username != 'test' or password != 'test':
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.route('/users/all', methods=["GET"])
@jwt_required
def get_all_users():
    all_users = ['bob', 'alice']
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify(err='unauthorized'), 403
    return jsonify(users=USERS), 200


@app.route('/records', methods=['GET'])
@jwt_required
def get_admin_records():
    all_users = ['bob', 'alice']
    current_user = get_jwt_identity()
    if current_user != 'admin':
        return jsonify(err='unauthorized'), 403
    admin_db_q()
    return jsonify(records=ADMIN_DATABASE), 200


@app.route('/record/<id>', methods=['GET'])
@jwt_required
def user_record(id):
    current_user = get_jwt_identity()
    user_record = USER_DATABASE.get(current_user)
    user_record_q(current_user)
    return jsonify(user_record=user_record), 200


def user_record_q(user):
    print(f'SELECT * FROM USER_DATABASE WHERE user={user}')


def admin_db_q():
    print(f'SELECT * FROM ADMIN_DATABASE')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
