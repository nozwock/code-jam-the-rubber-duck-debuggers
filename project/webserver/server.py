import random
import string

from flask import Flask, Request, Response, redirect, render_template, request


class WebServer(object):
    TOKEN_CHARS = string.ascii_letters

    def __init__(self, **configs):
        self.registered_tokens = {}
        self.rooms = {}
        self.configs(**configs)
        self.app = Flask(__name__)
        self.configure_endpoints()

    def configure_endpoints(self):
        """Adds all url endpoint with their respective server function."""
        self.add_endpoint("/", "home", self.home, methods=["GET"])

    def configs(self, **configs):
        for config, value in configs:
            self.app.config[config.upper()] = value

    def add_endpoint(
        self,
        endpoint=None,
        endpoint_name=None,
        handler=None,
        methods=None,
        *args,
        **kwargs
    ):
        if methods is None:
            methods = ["GET"]
        self.app.add_url_rule(
            endpoint, endpoint_name, handler, methods=methods, *args, **kwargs
        )

    def run(self, **kwargs):
        self.app.run(**kwargs)

    def generate_token(self, length=12) -> str:
        """Generate a random string for a session token."""
        while True:
            random_token = "".join(
                [random.choice(WebServer.TOKEN_CHARS) for _ in range(length)]
            )
            if random_token not in self.registered_tokens:
                return random_token

    def has_valid_token(self, request_obj: Request) -> bool:
        """Check if the request contains a valid session token."""
        # if the request has no session_token
        if "session_token" not in dict(request_obj.cookies):
            return False
        # if the session_token is not valid
        if request_obj.cookies["session_token"] not in list(
            self.registered_tokens.keys()
        ):
            return False
        # checks passed
        return True

    # Endpoint functions #

    def home(self) -> str | Response:
        """Landing page for starting a game."""
        room_id = request.args.get("r")
        if room_id:
            # player tries to access a room
            if room_id in self.rooms:
                # room exists
                room = self.rooms[room_id]
                if room.in_lobby:
                    # lobby
                    return render_template("lobby.html")
                elif room.playing:
                    # in-game
                    return render_template(type(room).HTML_FILE)
            else:
                # room does not exist (anymore)
                # redirect to homepage
                return redirect("/")
        else:
            # no room in url
            # return homepage to create new room
            return render_template("home.html")


server = WebServer()

if __name__ == "__main__":
    server.run(debug=True)
