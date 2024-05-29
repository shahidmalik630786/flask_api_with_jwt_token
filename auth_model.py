import json 
from flask import Flask, request, make_response,jsonify
from datetime import datetime,timedelta
import re
import jwt


class AuthModel:
    def __init__(self, mysql):
        self.mysql = mysql
        self.cur = mysql.connection.cursor()

    def token_auth(self,endpoint):
        def inner1(func):
            def inner2(*args):
                auth=(request.headers.get("authorization"))
                if re.match("^Bearer *([^/]+) *$",auth, flags=0):
                    split_auth = auth.split(" ")
                    token=split_auth[1]
                    try:
                        jwt_decode=(jwt.decode(token,"shahid",algorithms="HS256"))
                    except jwt.ExpiredSignatureError:
                        return make_response(jsonify({"message":"Token is expired"}), 401)
                    role_id=(jwt_decode["payload"])[0]
                    with self.mysql.connection.cursor() as cursor:
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
                else:
                    return make_response(jsonify({"Error":"Token invalid"}),401)
                
            return inner2
        return inner1