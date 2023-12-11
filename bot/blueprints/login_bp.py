from flask_login import LoginManager, login_user, logout_user, UserMixin, login_required
from flask import render_template, url_for, redirect, request, Blueprint

from config import ADMIN_PASSWORD, ADMIN_USERNAME

class User(UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.password = password


login_bp = Blueprint('login_bp', __name__)
login_manager = LoginManager()
login_manager.login_view = 'login_bp.login'


@login_bp.record_once
def init_app(state):
    login_manager.init_app(state.app)


@login_manager.user_loader
def load_user(user_id):
   if user_id == ADMIN_USERNAME:
       return User(user_id, ADMIN_PASSWORD)
   else:
       return None
   
# ! login route
@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            user = User(username, password)
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html', title='Login')

# ! logout route
@login_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_bp.login'))