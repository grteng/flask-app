from flask import Flask, render_template, redirect, url_for, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
login_manager = LoginManager(app)

# Mock user database
class User(UserMixin):
    users = {'user1': {'password': 'pass123', 'role': 'user'},
             'admin': {'password': 'adminpass', 'role': 'admin'}}

@login_manager.user_loader
def load_user(username):
    if username not in User.users:
        return None
    user = User()
    user.id = username
    return user

# WTForms Login Form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    submit = SubmitField('Login')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username in User.users and User.users[username]['password'] == password:
            user = load_user(username)
            login_user(user)
            flash(f'Logged in as {username}', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_authenticated and current_user.get_id() in User.users:
        role = User.users[current_user.get_id()]['role']
        return f'Welcome to the dashboard, {current_user.get_id()}! Your role is: {role}'
    return 'Unauthorized'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

