from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Group1(Resource):
    def get(self, group_id=None):
        if group_id:
            return group_id
        return ['admin', 'dev', 'paylink']
    
    def put(self, group_id=None):
        if group_id:
            return "new " + group_id
        return 'Please provide a groupId', 400

class Group2(Resource):
    def get(self, group_id, user_id=None):
        return ['snsakala', 'ckoenig']

class Users(Resource):
    def get(self):
        return ['snsakala', 'ckeonig', 'mgrof']

api.add_resource(Group1, '/groups', '/groups/<string:group_id>')
api.add_resource(Group2, '/groups/<string:group_id>/users')
api.add_resource(Users, '/users')

if __name__ == '__main__':
    app.run(debug=True)
