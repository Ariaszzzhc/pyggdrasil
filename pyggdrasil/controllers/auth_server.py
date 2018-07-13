from flask_restplus import Namespace, Resource
import uuid

auth_server_api = Namespace('authserver')


@auth_server_api.route('/authenticate')
class Authentication(Resource):
    def post(self):
        pass


@auth_server_api.route('/refresh')
class Refresh(Resource):
    def post(self):
        pass


@auth_server_api.route('/validate')
class Validation(Resource):
    def post(self):
        pass


@auth_server_api.route('/invalidate')
class Invalidation(Resource):
    def post(self):
        pass


@auth_server_api.route('/signout')
class SignOut(Resource):
    def post(self):
        pass

