import jinja2
import os
import webapp2
from google.appengine.ext import ndb
from webapp2_extras import sessions

import oauth2
import argparse
import json
import pprint
import sys
import urllib
import urllib2

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


API_HOST = 'api.yelp.com'
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'San Francisco, CA'
SEARCH_LIMIT = 5
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'

# OAuth credential placeholders that must be filled in by users.
CONSUMER_KEY = 'R62we9CE9OfSZ24KUSA5oQ'
CONSUMER_SECRET = 'w3Po8Mnhx0P3CNycvzr5nhGlSeQ'
TOKEN = '_3l2jIb_078LZvZvd4PpxWkXiRSJ69sB'
TOKEN_SECRET = 'P0qf6ykcRanGO4W7WADfLYZn7Lo'



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
        self.redirect("results")
        print self.session['food_types']

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

        term = self.session['food_types']
        location = '10460'

        results_by_term = {}
        for i in range(len(term)):
            term[i] = term[i].replace(' ', '+')

            url_params = {
                'term': term[i],
                'location': location.replace(' ', '+'),
                'limit': SEARCH_LIMIT,
                'category_filter': 'restaurants'
            }
            print "url_params {}".format(url_params)

            results_by_term[term[i]] = self.api_request(API_HOST,SEARCH_PATH, url_params=url_params)

        template = jinja_environment.get_template('results.html')
        self.response.write(template.render({'results_list' : results_by_term}))

    def api_request(self, host, path, url_params=None):
        """Prepares OAuth authentication and sends the request to the API.
        Args:
            host (str): The domain host of the API.
            path (str): The path of the API after the domain.
            url_params (dict): An optional set of query parameters in the request.
        Returns:
            dict: The JSON response from the request.
        Raises:
            urllib2.HTTPError: An error occurs from the HTTP request.
        """
        url_params = url_params or {}
        url = 'http://{0}{1}?'.format(host, urllib.quote(path.encode('utf8')))
        print 'params: {}'.format(url_params)

        consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
        oauth_request = oauth2.Request(method="GET", url=url, parameters=url_params)

        oauth_request.update(
            {
                'oauth_nonce': oauth2.generate_nonce(),
                'oauth_timestamp': oauth2.generate_timestamp(),
                'oauth_token': TOKEN,
                'oauth_consumer_key': CONSUMER_KEY
            }
        )
        token = oauth2.Token(TOKEN, TOKEN_SECRET)
        oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
        signed_url = oauth_request.to_url()

        print u'Querying {0} ...'.format(url)

        conn = urllib2.urlopen(signed_url, None)
        try:
            response = json.loads(conn.read())
        finally:
            conn.close()

        return response

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
