import mysql.connector
from flask import Flask, request, make_response,jsonify,request
from datetime import datetime,timedelta
import jwt
import re

def _get_database_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="flask_api"
    )
    return connection


class Database:
    def get_all_users():
        return_dict = {}
        _connection = _get_database_connection()
        try:
            cursor = _connection.cursor()
            cursor.execute('SELECT * FROM user')
            results = cursor.fetchall()
            cursor.close()
            _connection.commit()
            _connection.close()
            return_dict = {'success': True, 'data': results}
        except Exception as e:
            return_dict = {'success': False, 'msg': str(e)}
        finally:
            _connection.close()
        return return_dict
    
    '''This method allows you to perform crud by just passing query and parameters'''
    def database_operation(self, query_data):
        return_dict = {}
        _connection = _get_database_connection()
        try:
            _cursor = _connection.cursor()
            query, params = query_data  
            _cursor.execute(query, params)  
            _cursor.close()
            _connection.commit()
            _connection.close()
            return_dict = {'success': True, 'data': "success"}
        except Exception as e:
            return_dict = {'success': False, 'msg': str(e)}
        finally:
            _connection.close()
        return return_dict
            
    
    def user_login_details(self,data):
        return_dict = {}
        _connection = _get_database_connection()
        try:
            cursor = _connection.cursor()
            cursor.execute("SELECT * FROM user WHERE email=%s AND password=%s", (data.get('email'), data.get('password')))
            results = cursor.fetchall()
            cursor.close()
            return_dict = {'success': True, 'data': results}
        except Exception as e:
            return_dict = {'success': False, 'msg': str(e)}
        finally:
            _connection.close()
        return return_dict
    


'''In this method we have created a decorator which we are calling in controller.py before function runnibg here this function checks whether user embedded in jwt token has permission to access this function or not. Here it checks by getting the user id then chcking in table wheter this user is authorized for this function or not.'''

class Authorization:

    def token_auth(self,endpoint):
        def inner1(func):
            def inner2(*args):
                auth=(request.headers.get("authorization")) # fetching Authorization field where we put token 
                if re.match("^Bearer *([^/]+) *$",auth, flags=0):
                    split_auth = auth.split(" ")
                    token=split_auth[1] #access token from it
                    try:
                        jwt_decode=(jwt.decode(token,"shahid",algorithms="HS256")) #Here shahid is a secret key which we have used 
                                                                                  #to encode and now we are using to decoding
                    except jwt.ExpiredSignatureError:
                        return make_response(jsonify({"message":"Token is expired"}), 401)
                    role_id=(jwt_decode["payload"])[0]
                    return_dict = {}
                    _connection = _get_database_connection()
                    try:
                        cursor = _connection.cursor()
                        cursor.execute("SELECT roles FROM accessiblity_view WHERE endpoint=%s", (endpoint,))
                        result = cursor.fetchall()
                        if len(result) > 0:
                            allowed_role=((result[0][0][1]))
                            print(allowed_role,role_id)
                            if allowed_role == str(role_id):
                                return func(*args)
                            else:
                                return make_response(jsonify({'message': 'No access for this endpoint'}), 403)
                            
                        else:
                            return make_response(jsonify({'message': 'No access for this endpoint'}), 403)
                    except Exception as e:
                        return_dict = {'success': False, 'msg': str(e)}
                    finally:
                        _connection.close()
                    return return_dict
                else:
                    return make_response(jsonify({"Error":"Token invalid"}),401)
                
            return inner2
        return inner1


