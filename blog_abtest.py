from flask import Flask, jsonify, request, render_template, make_response, session
from db_model import mongodb
from db_model import mysql
from flask_login import LoginManager, current_user, login_user
from flask_cors import CORS
from blog_view import blog
from blog_control.user_mgmt import User
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__, static_url_path='/static')
CORS(app)
app.secret_key = os.urandom(24)

app.register_blueprint(blog.blog_abtest, url_prefix='/blog')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return make_response(jsonify(success=False), 401)

@app.before_request
def app_before_request():
    if 'client_id' not in session:
        session['client_id'] = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080", debug=True)