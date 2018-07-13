from flask_restplus import Namespace, Resource, reqparse

session_server_api = Namespace('sessionserver/session/minecraft')


@session_server_api.route('/join')
class Join(Resource):
    def post(self):
        pass


@session_server_api.route('/hasJoined')
class HasJoined(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username')
    parser.add_argument('serverId')
    parser.add_argument('ip')

    def get(self):
        args = self.parser.args()
        pass


@session_server_api.route('/profile/<id>')
class CharacterProfile(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('unsigned')

    def get(self, id):
        args = self.parser.args()
        pass


@session_server_api.route('/')
class CharacterProfileList(Resource):
    def post(self):
        pass
