from flask import Flask, request, jsonify,make_response
from flask_mysqldb import MySQL
from operations import Database,Authorization
import jwt
from datetime import datetime,timedelta

app = Flask(__name__)

auth = Authorization()


#returns all the data
@app.route('/data')
@auth.token_auth('/data')
def get_all_users():
    result = Database.get_all_users()
    return jsonify(result)


@app.route('/insert', methods=['POST'])
def insert_user():
    data = request.json
    query= 'INSERT INTO user (name, email, password, role, phone) VALUES (%s, %s, %s, %s, %s)'
    params = (data.get('name'), data.get('email'), data.get('password'), data.get('role'), data.get('phone'))
    user_model = Database() 
    result = user_model.database_operation((query, params))
    print(result)
    return jsonify(result)

@app.route('/update', methods=['PUT'])
def update_user():
    data = request.json
    query='UPDATE user SET name=%s, email=%s, password=%s, role=%s, phone=%s WHERE id=%s'
    params = (data.get('name'), data.get('email'), data.get('password'), data.get('role'), data.get('phone'),data.get('id'))
    user_model = Database()
    result =  user_model.database_operation((query, params))
    return jsonify(result)

@app.route('/delete', methods=['DELETE'])
def delete_user():
    data = request.json
    query='DELETE FROM user WHERE id=%s'
    params=(data.get('id'),)
    user_model = Database() 
    result =  user_model.database_operation((query, params))
    return jsonify(result)


'''This method run when user will login and jwt token will be generated and return'''
@app.route("/user/login", methods=['POST'])
def user_login():
    data = request.json
    user_model = Database() 
    result= user_model.user_login_details(data)
    userdata = (result.get('data'))[0]
    exp_time = datetime.now() + timedelta(minutes=15) #adding expiry time for jwt tke
    exp_epoc_time = int(exp_time.timestamp())
    payload = {'payload': userdata, 'exp': exp_epoc_time}
    token=jwt.encode(payload,"shahid",algorithm="HS256") #Here shahid is a secret key which we have used to encode and now we are using to decoding/
    if result:
        return make_response(jsonify({'token': token},200))
    else:
        return make_response(jsonify({"Invalid email or password", 401}))





if __name__ == "__main__":
    app.run(debug=True)























# @app.route('/insert', methods=['POST'])
# def insert_user():
#     data = request.json
#     query=query = query = 'INSERT INTO user (name, email, password, role, phone) VALUES (%s, %s, %s, %s, %s)'
#     params = (data.get('name'), data.get('email'), data.get('password'), data.get('role'), data.get('phone'))
#     return user_model.database_operation((query, params))

# @app.route('/update', methods=['PUT'])
# def update_user():
#     data = request.json
#     query='UPDATE user SET name=%s, email=%s, password=%s, role=%s, phone=%s WHERE id=%s'
#     params = (data.get('name'), data.get('email'), data.get('password'), data.get('role'), data.get('phone'),data.get('id'))
#     return user_model.database_operation((query, params))

# @app.route('/delete', methods=['DELETE'])
# def delete_user():
#     data = request.json
#     query='DELETE FROM user WHERE id=%s'
#     params=(data.get('id'),)
#     return user_model.database_operation((query, params))

# @app.route("/user/login", methods=['POST'])
# def user_login():
#     data = request.json
#     return user_model.user_login_details(data)

