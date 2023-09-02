from flask import Flask, render_template, request

class WebServer(object):
  def __init__(self, **configs):
    self.registered_cookies = {}
    self.configs(**configs)
    self.app = Flask(__name__)
    self.configure_endpoints()
    self.app.after_request(self.after_request)
  
  def configure_endpoints(self):
    """ add all url endpoint with their respective server function """
    self.add_endpoint('/', 'homepage', self.homepage, methods=['GET'])

  def configs(self, **configs):
    for config, value in configs:
        self.app.config[config.upper()] = value

  def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET'], *args, **kwargs):
    self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)

  def run(self, **kwargs):
    self.app.run(**kwargs)
  
  def generate_cookie(self, length=12):
    ''' Generate a random string for a session cookie. '''
    while True:
      random_cookie = ''.join([random.choice(COOKIE_CHARS) for _ in range(length)])
      if not random_cookie in self.registered_cookies:
        return random_cookie
  
  ## Endpoint functions ##

  def homepage(self):
    ''' The endpoint for the homepage. '''
    return render_template("home.html")
  
  def after_request(self, response):
    ''' Check if the connected user has a valid SessionCookie. '''
    if not 'session_id' in dict(request.cookies):
      # no session_id yet,
      # give a session cookie
      response.set_cookie('session_id', self.generate_cookie())
      return response


server = WebServer()

if __name__ == "__main__":
  server.run(debug=True)
