import jinja2
import os
import webapp2
from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('homepage.html')
        self.response.write(template.render())

class Question1Handler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('questions-form.html')
        self.response.write(template.render())

class SaveHandler(webapp2.RequestHandler):
    def post(self):
        food_types = self.request.get('food', allow_multiple=True)
        print(food_types)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/questions-form.html', Question1Handler),
    ('/save', SaveHandler)
    # ('/count', CountHandler)
], debug=True)
