import jinja2
import os
import webapp2
from google.appengine.ext import ndb
from webapp2_extras import sessions

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

food_types = []
food_prices = []
food_other = []
food_attire = []
food_service = []
food_distance = []
food_reservation = []
results = {}

class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'my-super-secret-key',
}

class MainHandler(BaseHandler):
    def get(self):
        template = jinja_environment.get_template('homepage.html')
        self.response.write(template.render())

class TypeHandler(BaseHandler):
    def get(self):
        template = jinja_environment.get_template('questions-form.html')
        self.response.write(template.render())

    def post(self):
        self.session['food_types'] = self.request.get_all('type')
        self.redirect("foodprice")

class PricesHandler(BaseHandler):
    def get(self):
        template = jinja_environment.get_template('questions-form-price.html')
        self.response.write(template.render())

    def post(self):
        self.session['food_prices'] = self.request.get_all('price')
        self.redirect('fooddistance')

class DistanceHandler(BaseHandler):
    def get(self):
        template = jinja_environment.get_template('questions-form-distance.html')
        self.response.write(template.render())

    def post(self):
        self.session['food_distance'] = self.request.get('distance')
        self.redirect('foodattire')

class AttireHandler(BaseHandler):
    def get(self):
        template = jinja_environment.get_template('questions-form-attire.html')
        self.response.write(template.render())

    def post(self):
        self.session['food_attire'] = self.request.get_all('attire')
        self.redirect('foodservice')

class ServiceHandler(BaseHandler):
    def get(self):
        template = jinja_environment.get_template('questions-form-service.html')
        self.response.write(template.render())

    def post(self):
        self.session['food_service'] = self.request.get_all('service')
        self.redirect('foodreservation')

class ReservationHandler(BaseHandler):
    def get(self):
        template = jinja_environment.get_template('questions-form-reservation.html')
        self.response.write(template.render())

    def post(self):
        self.session['food_reservation'] = self.request.get_all('reservation')
        self.redirect('foodother')

class OtherHandler(BaseHandler):
    def get(self):
        template = jinja_environment.get_template('questions-form-other-questions.html')
        self.response.write(template.render())

    def post(self):
        self.session['food_other'] = self.request.get_all('other_requirements')
        self.redirect('results')

class ResultsHandler(BaseHandler):
    def get(self):
        template = jinja_environment.get_template('results.html')
        self.response.write(template.render({'results_list' : self.session}))

class DeveloperHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('developers.html')
        self.response.write(template.render())

class ReferenceHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('references.html')
        self.response.write(template.render())


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/foodtype', TypeHandler),
    ('/foodprice', PricesHandler),
    ('/fooddistance', DistanceHandler),
    ('/foodattire', AttireHandler),
    ('/foodservice', ServiceHandler),
    ('/foodreservation', ReservationHandler),
    ('/foodother', OtherHandler),
    ('/results', ResultsHandler),
    ('/developers', DeveloperHandler),
    ('/references', ReferenceHandler)
], config=config, debug=True)
