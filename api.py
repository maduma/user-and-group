from flask import Flask
from flask_restful import Resource, Api, reqparse
import uuid

app = Flask(__name__)
api = Api(app)

auth = {}
groups = {'admin': ['snsakala', 'ckoenig'], 'dxretail': ['ckoenig']}

class Group1(Resource):
    def get(self, group_id=None):
        if group_id:
            if group_id in groups:
                return { group_id: groups[group_id] }
            return { 'message': 'cannot find group ' + group_id}, 404
        return groups.keys()
    
    def put(self, group_id=None):
        if group_id:
            groups[group_id] = []
            return { 'message': group_id + ' created'}
        return { 'message': 'Please provide a groupId'}, 400

    def delete(self, group_id=None):
        if not group_id:
            return { 'message': 'please provide group_id' }
        if group_id in groups:
            if len(groups[group_id]) == 0:
                groups.pop(group_id)
                return { 'message': 'group delete' }
            return { 'message': 'group not empty' }, 400
        return { 'message': 'group not existing'} 

class Group2(Resource):
    def get(self, group_id):
        if group_id in groups:
            return groups[group_id] 
        return { 'message': 'cannot find group ' + group_id}, 404

class Group3(Resource):
    def put(self, group_id, user_id):
        if group_id in groups:
            if user_id not in groups[group_id]:
                groups[group_id].append(user_id)
                return groups[group_id] 
            return { 'message': 'user already in group'}
        return { 'message': 'cannot find group ' + group_id}, 404

    def delete(self, group_id, user_id):
        if group_id in groups:
            if user_id in groups[group_id]:
                groups[group_id].remove(user_id)
                return { 'message': 'user removed from group' } 
            return { 'message': 'cannot find user ' + user_id}, 404
        return { 'message': 'cannot find group ' + group_id}, 404

class Users1(Resource):
    def get(self):
        users = []
        for group_id in groups:
            for user_id in groups[group_id]:
                if not user_id in users:
                    users.append(user_id)
        return users

class Users2(Resource):
    def get(self, user_id):
        users = []
        for group_id in groups:
            for user in groups[group_id]:
                if not user in users:
                    users.append(user)
        if user_id in users:
            return user_id
        return { 'message': 'cannot find user' }, 404

class Users3(Resource):
    def get(self, user_id):
        user_groups = []
        for group_id in groups:
            if user_id in groups[group_id]:
                user_groups.append(group_id)
        return user_groups

class Login(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True)
    parser.add_argument('password', required=True)

    def post(self):
        args = self.parser.parse_args()
        if args['username'] == 'snsakala' and args['password'] == 'Luxair123':
            auth['username'] = args['username']
            auth['token'] = str(uuid.uuid4())
            return auth['token']
        return { 'message': 'access denied'}, 403

class Logout(Resource):
    def get(self):
        auth = {}
        return { 'message': 'logged out'}

api.add_resource(Group1, '/groups', '/groups/<string:group_id>')
api.add_resource(Group2, '/groups/<string:group_id>/users')
api.add_resource(Group3, '/groups/<string:group_id>/users/<string:user_id>')
api.add_resource(Users1, '/users')
api.add_resource(Users2, '/users/<string:user_id>')
api.add_resource(Users3, '/users/<string:user_id>/groups')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')

if __name__ == '__main__':
    app.run(debug=True)

class Users(Resource):
    def get(self):
        return ['snsakala', 'ckeonig', 'mgrof']

class Login(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True)
    parser.add_argument('password', required=True)

    def post(self):
        args = self.parser.parse_args()
        if args['username'] == 'snsakala' and args['password'] == 'Luxair123':
            auth['username'] = args['username']
            auth['token'] = str(uuid.uuid4())
            return auth['token']
        return { 'message': 'access denied'}, 403

class Logout(Resource):
    def get(self):
        auth = {}
        return { 'message': 'logged out'}

api.add_resource(Group1, '/groups', '/groups/<string:group_id>')
api.add_resource(Group2, '/groups/<string:group_id>/users')
api.add_resource(Group3, '/groups/<string:group_id>/users/<string:user_id>')
api.add_resource(Users, '/users')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')

if __name__ == '__main__':
    app.run(debug=True)
