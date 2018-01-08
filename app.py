import httplib2
import os

from google.appengine.ext import webapp
from google.appengine.api import memcache
from apiclient.discovery import build
from oauth2client.contrib.appengine import OAuth2DecoratorFromClientSecrets

CLIENT_SECRETS = os.path.join(os.path.dirname(os.path.dirname(__file__)),
    'client_secrets.json')

decorator = OAuth2DecoratorFromClientSecrets(CLIENT_SECRETS, 'https://www.googleapis.com/auth/calendar')

# Helpful message to display in the browser if the CLIENT_SECRETS file
# is missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
<h1>Warning: Please configure OAuth 2.0</h1>
<p>
To make this sample run you will need to populate the client_secrets.json file
found at:
</p>
<p>
<code>%s</code>.
</p>
<p>with information found on the <a
href="https://code.google.com/apis/console">APIs Console</a>.
</p>
""" % CLIENT_SECRETS

http = httplib2.Http(memcache)
service = build('calendar', 'v3', http=http)

class MainHandler(webapp.RequestHandler):

    @decorator.oauth_aware
    def get(self):
        if decorator.has_credentials():
            import json
            from cal.main import update_cal

            removed, added, updated = update_cal(service)

            result = { 'removed': removed, 'added': added, 'updated': updated }

            self.response.headers['Content-Type'] = 'text/json'
            self.response.write(json.dumps(result))

        else:
            url = decorator.authorize_url()
            self.render_response('oauth2_error.html', text=MISSING_CLIENT_SECRETS_MESSAGE)

app = webapp2.WSGIApplication([
     ('/', MainHandler),
     (decorator.callback_path, decorator.callback_handler())], debug=True)
