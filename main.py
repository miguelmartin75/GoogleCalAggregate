import webapp2

from google.auth import app_engine
import googleapiclient.discovery

credentials = app_engine.Credentials()
service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

# Helpful message to display in the browser if the CLIENT_SECRETS file
# is missing.
#MISSING_CLIENT_SECRETS_MESSAGE = """
#<h1>Warning: Please configure OAuth 2.0</h1>
#<p>
#To make this sample run you will need to populate the client_secrets.json file
#found at:
#</p>
#<p>
#<code>%s</code>.
#</p>
#<p>with information found on the <a
#href="https://code.google.com/apis/console">APIs Console</a>.
#</p>
#""" % CLIENT_SECRETS

class HealthCheckHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('OK')

class UpdateHandler(webapp2.RequestHandler):
    def get(self):
        import json
        from cal.main import update_cal

        removed, added, updated = update_cal(service)

        result = { 'removed': removed, 'added': added, 'updated': updated }
        self.response.headers['Content-Type'] = 'text/json'
        self.response.write(json.dumps(result))

        #if decorator.has_credentials():
        #else:
        #    url = decorator.authorize_url()
        #    self.response.write('Please click <a href="{}"">here</a> to authorize.'.format(url))


app = webapp2.WSGIApplication([
    ('/', HealthCheckHandler),
    ('/update', UpdateHandler)#,
    #(decorator.callback_path, decorator.callback_handler())
], debug=True)
