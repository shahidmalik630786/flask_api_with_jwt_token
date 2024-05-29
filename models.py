# import json 
# from flask import Flask, request, make_response
# from datetime import datetime,timedelta
# import jwt



# class UserModel:
#     def __init__(self, mysql):
#         self.mysql = mysql

#     def get_all_users(self, ):
#         cur = self.mysql.connection.cursor()
#         cur.execute('SELECT * FROM user')
#         column_names = [i[0] for i in cur.description]
#         results = cur.fetchall()
#         cur.close()
#         res= make_response({'payload': results},200)
#         res.headers['Access-Control-Allow-Origin'] = '*'
#         return res
    

#     def database_operation(self, query_data):
#         cur = self.mysql.connection.cursor()
#         query, params = query_data  
#         cur.execute(query, params)  
#         self.mysql.connection.commit()
#         cur.close()
#         return make_response({'message': "Operation performed successfully"}, 200)

#     def user_login_details(self, data):
#         cur = self.mysql.connection.cursor()
#         cur.execute("SELECT * FROM user WHERE email=%s AND password=%s", (data.get('email'), data.get('password')))
#         user = cur.fetchall()
#         self.mysql.connection.commit()
#         cur.close()
#         userdata = user[0]
#         exp_time = datetime.now() + timedelta(minutes=15)
#         exp_epoc_time = int(exp_time.timestamp())
#         payload = {'payload': userdata, 'exp': exp_epoc_time}
#         token=jwt.encode(payload,"shahid",algorithm="HS256")
#         if user:
#             return make_response({'token': token},200)
#         else:
#             return "Invalid email or password", 401















# # def insert_user(self, name, email, password, role, phone):
#     #     cur = self.mysql.connection.cursor()
#     #     cur.execute(
#     #         'INSERT INTO user (name, email, password, role, phone) VALUES (%s, %s, %s, %s, %s)',
#     #         (name, email, password, role, phone)
#     #     )
#     #     self.mysql.connection.commit()
#     #     cur.close()
#     #     res= make_response({'payload': "User inserted successfully"},200)
#     #     res.headers['Access-Control-Allow-Origin'] = '*'
#     #     return res


#     # def update_user(self, user_id, name, email, password, role, phone):
#     #     cur = self.mysql.connection.cursor()
#     #     cur.execute(
#     #         'UPDATE user SET name=%s, email=%s, password=%s, role=%s, phone=%s WHERE id=%s',
#     #         (name, email, password, role, phone, user_id)
#     #     )
#     #     self.mysql.connection.commit()
#     #     cur.close()
#     #     res= make_response({'payload': "User updated successfully"},201)
#     #     res.headers['Access-Control-Allow-Origin'] = '*'
#     #     return res

#     # def delete_user(self, user_id):
#     #     cur = self.mysql.connection.cursor()
#     #     cur.execute('DELETE FROM user WHERE id=%s', (user_id,))
#     #     self.mysql.connection.commit()
#     #     cur.close()
#     #     return make_response({'status': 'User deleted successfully'})