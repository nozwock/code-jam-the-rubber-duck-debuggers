from flask import Flask, request, Request, Response, render_template
import string
import random
import room
from flask_socketio import SocketIO


class GameModeNotFoundError(Exception):
    ...


class GameApi(object):
    TOKEN_CHARS = string.ascii_letters

    def __init__(self, **configs):
        self.registered_tokens = {}
        self.rooms = {"secret-dog": room.Classic()}
        self.configs(**configs)
        self.app = Flask(__name__)
        self.socketio = SocketIO()
        self.socketio.init_app(self.app, cors_allowed_origins="http://127.0.0.1:5000")
        self.configure_endpoints()
        socketio = self.socketio
        @socketio.on("connect")
        def handle_connect():
            print('Client connected')

    def configure_endpoints(self):
        """Adds all url endpoint with their respective server function."""
        self.add_endpoint('/api/get_room_settings', 'room_settings', self.get_room_settings, methods=['GET'])
        self.add_endpoint('/api/create_room', 'create_room', self.create_room, methods=['POST'])
        self.add_endpoint('/', 'homepage', self.homepage, methods=['GET'])

        self.app.after_request(self.after_request)

    def configs(self, **configs):
        for config, value in configs:
            self.app.config[config.upper()] = value

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=None, *args, **kwargs):
        if methods is None:
            methods = ["GET"]
        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)

    def run(self, **kwargs):
        self.app.run(**kwargs)

    def generate_token(self, length=12) -> str:
        """Generate a random string for a session token."""
        while True:
            random_token = ''.join([random.choice(GameApi.TOKEN_CHARS) for _ in range(length)])
            if random_token not in self.registered_tokens:
                return random_token

    def get_player_token(self, request: Request) -> str:
        return request.cookies['token']

    def has_valid_token(self, request_obj: Request) -> bool:
        """Check if the request contains a valid session token."""
        # if the request has no session_token
        if 'session_token' not in dict(request_obj.cookies):
            return False
        # if the session_token is not valid
        if request_obj.cookies['session_token'] not in list(self.registered_tokens.keys()):
            return False
        # checks passed
        return True

    def get_gamemode(self, gamemode_name: str) -> object:
        """Get a room class by the gamemodes name."""
        for gamemode in room.GAMEMODES:
            if gamemode.__name__ == gamemode_name:
                return gamemode
        # no gamemode found
        raise GameModeNotFoundError

    #### API ENDPOINTS ####
    def homepage(self):
        return render_template('home.html')

    def after_request(self, response: Response):
        """Validate the response before sending to the client."""
        print(request.cookies)
        if not request.cookies.get('token'):
            response.set_cookie('token', self.generate_token())
        return response

    def get_room_settings(self) -> dict:
        """An API call to recieve the settings of a room."""
        room_id = request.args.get('room_id')
        if room_id and room_id in self.rooms:
            room = self.rooms[room_id]
            return {"success": True, "message": "success!", "data": room.get_settings()}
        else:
            return {"success": False, "message": "You did not provide a valid room id."}

    def create_room(self) -> dict:
        """Create a room, based on the gamemode's name."""
        # get gamemode
        data = request.get_json(force=True)
        gamemode_name = data['gamemode']
        # create room
        try:
            Gamemode = self.get_gamemode(gamemode_name)
            room = Gamemode()
            return {"success": True, "message": "Success!", "room_id": room.id}
        except GameModeNotFoundError:
            return {"success": False, "message": "Gamemode was not found!"}

    def join_room(self) -> dict:
        """An API call to join a room."""
        data = request.get_json(force=True)
        room_id = data["room_id"]
        try:
            room = self.rooms[room_id]
        except KeyError:
            return {"success": False, "message": "Room not found."}
        player_id = self.get_player_token(request)
        success = room.join(player_id)
        return {"success": success}


api = GameApi()

if __name__ == "__main__":
    api.socketio.run(api.app, debug=True)
