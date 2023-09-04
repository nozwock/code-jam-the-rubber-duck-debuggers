from flask import Flask, render_template
from extension import generate_socketio
import string
import room


class GameModeNotFoundError(Exception):
    ...


class GameApi:
    TOKEN_CHARS = string.ascii_letters

    def __init__(self, **configs):
        self.configs(**configs)
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'secret!'
        self.socketio = generate_socketio(self.app)

        self.configure_endpoints()

    def configure_endpoints(self):
        """Development function to add an webserver endpoint."""
        # TODO: replace with frontend server
        self.add_endpoint('/', 'homepage', self.homepage, methods=['GET'])

    def configs(self, **configs):
        for config, value in configs:
            self.app.config[config.upper()] = value

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=None, *args, **kwargs):
        if methods is None:
            methods = ["GET"]
        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)

    def run(self, **kwargs):
        """Start the socketio server."""
        self.socketio.run(self.app, **kwargs)

    #### ENDPOINTS ####

    def homepage(self):
        """Debug function to spin up a webserver."""
        # TODO: replace with fronend server
        return render_template('home.html')


api = GameApi()

if __name__ == "__main__":
    api.socketio.run(api.app, debug=True)
