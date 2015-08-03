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

class TypeHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('questions-form.html')
        self.response.write(template.render())

    def post(self):
        food_types = self.request.get_all('type')
        self.redirect("foodprice")

class PricesHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('questions-form-price.html')
        self.response.write(template.render())

    def post(self):
        food_prices = self.request.get_all('price')
        self.redirect('fooddistance')

class DistanceHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('questions-form-distance.html')
        self.response.write(template.render())

    def post(self):
        food_distance = self.request.get('distance')
        self.redirect('foodattire')

class AttireHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('questions-form-attire.html')
        self.response.write(template.render())

    def post(self):
        food_attire = self.request.get_all('attire')
        self.redirect('foodservice')

class ServiceHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('questions-form-service.html')
        self.response.write(template.render())

    def post(self):
        food_service = self.request.get_all('service')
        self.response.write(food_service)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/foodtype', TypeHandler),
    ('/foodprice', PricesHandler),
    ('/fooddistance', DistanceHandler),
    ('/foodattire', AttireHandler),
    ('/foodservice', ServiceHandler)
], debug=True)
