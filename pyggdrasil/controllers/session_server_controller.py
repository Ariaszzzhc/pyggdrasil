from flask import Blueprint


session_server_controller = Blueprint(
    'session_server_controller',
    __name__,
    url_prefix='/sessionserver'
)


@session_server_controller.route('/session/minecraft/join', methods=['POST'])
def join():
        pass


@session_server_controller.route('/session/minecraft/hasJoined', methods=['GET'])
def has_joined():
        pass


@session_server_controller.route('/session/minecraft/profile/<int:id>', methods=['GET'])
def get_character_profile(id):
        pass


@session_server_controller.route('/session/minecraft/', methods=['POST'])
def get_character_profile_list():
        pass
