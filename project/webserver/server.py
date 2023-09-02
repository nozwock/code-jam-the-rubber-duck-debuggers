from flask import Flask, render_template, request, redirect
import string
import random


class WebServer(object):
    TOKEN_CHARS = string.ascii_letters

    def __init__(self, **configs):
        self.registered_tokens = {}
        self.rooms = {}
        self.configs(**configs)
        self.app = Flask(__name__)
        self.configure_endpoints()
        self.app.before_request(self.before_request)

    def configure_endpoints(self):
        """ Adds all url endpoint with their respective server function. """
        self.add_endpoint('/', 'home', self.home, methods=['GET'])

    def configs(self, **configs):
        for config, value in configs:
            self.app.config[config.upper()] = value

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET'], *args, **kwargs):
        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)

    def run(self, **kwargs):
        self.app.run(**kwargs)

    def generate_token(self, length=12) -> str:
        ''' Generate a random string for a session token. '''
        while True:
            random_token = ''.join([random.choice(WebServer.TOKEN_CHARS) for _ in range(length)])
            if random_token not in self.registered_tokens:
                return random_token

    def has_valid_token(self, request: object) -> bool:
        ''' Check if the request contains a valid session token. '''
        # if the request has no session_token
        if 'session_token' not in dict(request.cookies):
            return False
        # if the session_token is not valid
        if request.cookies['session_token'] not in list(self.registered_tokens.keys()):
            return False
        # checks passed
        return True

    #### Endpoint functions ####

    def home(self) -> str:
        ''' Landing page for starting a game. '''
        room_id = request.args.get('r')
        if room_id:
            # player tries to access a room
            if room_id in self.rooms:
                # room exists
                room = self.rooms[room_id]
                if room.in_lobby:
                    # lobby
                    return render_template('lobby.html')
                elif room.playing:
                    # in-game
                    return render_template('playing.html')
            else:
                # room does not exist (anymore)
                # redirect to homepage
                return redirect('/')
        else:
            # no room in url
            # return homepage to create new room
            return render_template("home.html")


server = WebServer()

if __name__ == "__main__":
    server.run(debug=True)
