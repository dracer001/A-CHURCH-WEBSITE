from flask import Flask, session, send_from_directory


import os
from datetime import datetime

from dotenv import load_dotenv
from routes import public, admin, blog


load_dotenv()
secrete_key = os.getenv('SECRETE_KEY')
mongo_uri = os.getenv('MONGO_URI_DEV')


app = Flask(__name__, instance_relative_config=True, template_folder='views/templates', static_folder='views/static')
app.config['MONGO_URI'] = mongo_uri
app.secret_key = secrete_key
app.register_blueprint(public.public)
app.register_blueprint(admin.admin)
app.register_blueprint(blog.blog)


@app.template_filter('format_date')
def format_date(value):
    date_obj = datetime.strptime(value, '%Y-%m-%d')
    return date_obj.strftime('%B %d, %Y')


@app.template_filter('format_datetime')
def format_datetime(value):
    # date_obj = datetime.strptime(value, '%Y-%m-%d')
    return value.strftime('%b %d, %Y')


app.jinja_env.filters['format_date'] = format_date
app.jinja_env.filters['format_datetime'] = format_datetime


@app.route('/media/<path:filename>')
def media(filename):
    return send_from_directory('/views/media', filename)
# # def create_app(test_config=None):
#     # create and configure the app
#     app.config.from_mapping(
#         SECRET_KEY=secrete_key,
#     )

#     if test_config is None:
#         # load the instance config, if it exists, when not testing
#         app.config.from_pyfile('config.py', silent=True)
#     else:
#         # load the test config if passed in
#         app.config.from_mapping(test_config)

#     # ensure the instance folder exists
#     try:
#         os.makedirs(app.instance_path)
#     except OSError:
#         pass

#     with app.app_context():
#         app.config["MONGO_URI"] = uri
#         mongo = PyMongo(app)
#         g.mongo = mongo

#     return app
