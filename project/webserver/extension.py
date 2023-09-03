from flask_socketio import SocketIO


def generate_socketio(app):
    socketio = SocketIO(app, async_mode='eventlet')
    socketio.init_app(app, cors_allowed_origins="http://127.0.0.1:5000")

    @socketio.on("connect")
    def handle_connect():
        print('Client connected')

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected.')

    @socketio.on('my event')
    def handle_join(data):
        print('user' + str(data))

    return socketio
