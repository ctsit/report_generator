"""
This class implements a demo web app for retrieving data
about RED-I sites from an sqlite database.

To run the application:
    $ python rediapi.py
    $ curl http://127.0.0.1:5000/api/site/1
"""
__author__ = "University of Florida CTS-IT Team"
__copyright__ = "Copyright 2014, University of Florida"
__license__ = "BSD 3-Clause"

import os
import json
import urlparse
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.utils import redirect
from werkzeug.serving import run_simple
from jinja2 import Environment, FileSystemLoader

from datetime import datetime
import redidao

from period import Period

class RediApi(object):

    def __init__(self, config):
        """
        Define the routing rules for the application:

        https://github.com/mitsuhiko/werkzeug/blob/master/werkzeug/routing.py
        DEFAULT_CONVERTERS = {
            'default':          UnicodeConverter,
            'string':           UnicodeConverter,
            'any':              AnyConverter,
            'path':             PathConverter,
            'int':              IntegerConverter,
            'float':            FloatConverter,
            'uuid':             UUIDConverter,
        }
        """
        # @TODO: init the db connection
        self.db = config['db_file']
        self.template_show_api_summary = 'show_api_summary.html'
        self.template_show_index = 'index.html'

        template_path = os.path.join(os.path.dirname(__file__), 'templates')
        self.jinja_env = Environment(loader=FileSystemLoader(template_path), autoescape=True)

        # Add routes
        self.url_map = Map([
            Rule('/',                                   endpoint = 'show_index'),
            Rule('/api',                                endpoint = 'show_api_summary'),
            Rule('/api/',                               endpoint = 'show_api_summary'),
            Rule('/api/projects/',                      endpoint = 'get_projects'),
            Rule('/api/projects',                       endpoint = 'get_projects'),
            Rule('/api/project_sites/<int:project_id>', endpoint = 'get_project_sites'),

            Rule('/api/site_data/by_week/<int:site_id>',            endpoint = 'get_site_data_by_week'),
            Rule('/api/site_data/by_week_and_form/<int:site_id>',   endpoint = 'get_site_data_by_week_and_form'),
            Rule('/api/site_data/by_month/<int:site_id>',           endpoint = 'get_site_data_by_month'),
            Rule('/api/site_data/by_month_and_form/<int:site_id>',  endpoint = 'get_site_data_by_month_and_form'),
            Rule('/api/site_data/by_year/<int:site_id>',            endpoint = 'get_site_data_by_year'),
            Rule('/api/site_data/by_year_and_form/<int:site_id>',   endpoint = 'get_site_data_by_year_and_form'),
            Rule('/api/site_data/last_two_periods/<int:site_id>',   endpoint = 'get_site_data_for_last_two_periods'),
            Rule('/api/summary_data/<int:project_id>', endpoint = 'get_summary_data'),
            Rule('/api/site_details/<int:site_id>',     endpoint = 'get_site_details'),
        ])


    def error_404(self):
        """
        Generate output in case of errors
        @see #dispatch_request()
        """
        response = self.render_template('404.html')
        response.status_code = 404
        return response

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, 'on_' + endpoint)(request, **values)
        except NotFound, e:
            return self.error_404()
        except HTTPException, e:
            return e

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def render_template(self, template_name, **context):
        template = self.jinja_env.get_template(template_name)
        return Response(template.render(context), mimetype='text/html')

    def render_json(self, data):
        """
        Transform the received data structure into a json object
        """
        # @TODO: check if it is fine for long strings
        # https://docs.python.org/2/library/json.html
        # @see ensure_ascii=True
        return Response(json.dumps(data), mimetype='application/json')

    """ == Functions serving the defined routes """
    def on_show_api_summary(self, request):
        return self.render_template(self.template_show_api_summary, template_data={})

    def on_show_index (self, request):
        # Pass two period instances to the template for display
        curr = Period('curr_week')
        prev = Period('prev_week')
        periods = { 'curr': curr, 'prev' : prev}
        birthday = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
        return self.render_template(self.template_show_index, periods=periods, birthday=birthday)


    def on_get_projects(self, request):
        return self.render_json(redidao.get_projects(self.db))

    def on_get_project_sites(self, request, project_id):
        return self.render_json(redidao.get_project_sites(self.db, project_id))


    def on_get_site_data_by_week(self, request, site_id):
        return self.render_json(redidao.get_site_data(self.db, site_id, 'week', 0))

    def on_get_site_data_by_week_and_form(self, request, site_id):
        return self.render_json(redidao.get_site_data(self.db, site_id, 'week', 1))

    def on_get_site_data_by_month(self, request, site_id):
        return self.render_json(redidao.get_site_data(self.db, site_id, 'month', 0))

    def on_get_site_data_by_month_and_form(self, request, site_id):
        return self.render_json(redidao.get_site_data(self.db, site_id, 'month', 1))

    def on_get_site_data_by_year(self, request, site_id):
        return self.render_json(redidao.get_site_data(self.db, site_id, 'year', 0))

    def on_get_site_data_by_year_and_form(self, request, site_id):
        return self.render_json(redidao.get_site_data(self.db, site_id, 'year', 1))

    def on_get_site_data_for_last_two_periods(self, request, site_id):
        return self.render_json(redidao.get_site_data_for_last_two_periods(self.db, site_id))

    def on_get_site_details(self, request, site_id):
        return self.render_json(redidao.get_site_details(self.db, site_id))

    def on_get_summary_data(self, request, project_id):
        return self.render_json(redidao.get_summary_data(self.db, project_id))


def create_app(db_file, with_static=True):
    app = RediApi( { 'db_file': db_file })
    if with_static:
        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/_js':     os.path.join(os.path.dirname(__file__), 'static/_js'),
            '/_css':    os.path.join(os.path.dirname(__file__), 'static/_css'),
            '/_img':    os.path.join(os.path.dirname(__file__), 'static/_img'),
        })
    return app

if __name__ == '__main__':
    # @TODO: add configuration for database file name
    app_db_file = 'redi_runs.db'
    app_port = 5000
    app = create_app(app_db_file)
    run_simple('127.0.0.1', app_port, app, use_debugger=True, use_reloader=True)
