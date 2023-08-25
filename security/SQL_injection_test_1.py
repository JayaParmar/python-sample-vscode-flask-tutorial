from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, validators
from flask_wtf.csrf import CSRFProtect
import os
import base64

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

# Generate a CSRF token (example)
def generate_csrf_token():
    token = base64.urlsafe_b64encode(os.urandom(24)).decode('utf-8')
    return token

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)

class UserForm(Form):
    username = StringField('Username', [validators.InputRequired()])

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    form = UserForm(request.form)
    csrf_token = generate_csrf_token()
    if request.method == 'POST' and form.validate():
        new_user = User(username=form.username.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/users')
    return render_template('add_user.html', form=form, csrf_token=csrf_token)

@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
