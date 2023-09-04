"""extension.py is the socketio addition to the flask server."""

from flask_socketio import SocketIO
import game_handler


def generate_socketio(app):
    """Create the SocketIO app, based on a flask app."""
    socketio = SocketIO(app, async_mode='eventlet')
    socketio.init_app(app, cors_allowed_origins="http://127.0.0.1:5000")

    @socketio.on("connect")
    def handle_connect():
        print('Client connected')

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected.')

    @socketio.on('create_room')
    def handle_create_room(data: dict):
        """SocketIO handler for creating a new room.
        data: {
            "token": str
            "gamemode_name": str
        }
        """
        print('creating new room' + str(data))
        game_handler.create_room(data['gamemode_name'])

    return socketio
