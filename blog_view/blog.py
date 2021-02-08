from flask import Flask, Blueprint, request, render_template, jsonify, make_response, redirect, url_for, session
from blog_control.user_mgmt import User
from blog_control.session_mgmt import BlogSession
from flask_login import login_user, current_user, logout_user
import datetime

blog_abtest = Blueprint('blog', __name__)

@blog_abtest.route('/set_email', methods=['GET', 'POST'])
def set_email():
    if request.method == 'GET':
        # print('GET SET_EMAIL>>>>>', request.args.get('user_email'))
        return redirect(url_for('blog.test_blog'))
    else:
        # print('POST SET_EMAIL>>>>>', request.headers)
        # content type이 application/json인 경우
        # print('POST SET_EMAIL>>>>>', request.get_json())
        # print('POST SET_EMAIL>>>>>', request.form)
        # print('POST SET_MAIL>>>>>>', request.form['user_email'])
        user = User.create(request.form['user_email'], request.form['blog_id'])
        login_user(user, remember=True, duration=datetime.timedelta(days=365))

        return redirect(url_for('blog.test_blog'))

@blog_abtest.route('/logout')
def logout():
    User.delete(current_user.id)
    logout_user()
    return redirect(url_for('blog.test_blog'))

@blog_abtest.route('/test_blog')
def test_blog():
    if current_user.is_authenticated:
        webpage_name = BlogSession.get_blog_page(current_user.blog_id)
        BlogSession.save_session_info(session['client_id'], current_user.user_email, webpage_name)
        return render_template(webpage_name, user_email=current_user.user_email)
    else:
        webpage_name = BlogSession.get_blog_page()
        BlogSession.save_session_info(session['client_id'], 'anonymous', webpage_name)
        return render_template(webpage_name)