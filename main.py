import webapp2

from google.auth import app_engine
import googleapiclient.discovery

credentials = app_engine.Credentials()
service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

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

app = webapp2.WSGIApplication([
    ('/', HealthCheckHandler),
    ('/update', UpdateHandler)#,
], debug=True)
