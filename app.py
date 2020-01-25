from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/login', methods=['POST', 'GET'])
def do_admin_login():
    if request.method == 'POST':
        POST_USERNAME = str(request.form['username'])
        POST_PASSWORD = str(request.form['password'])
        query = db.session.query(User).filter_by(username=POST_USERNAME,password=POST_PASSWORD)
        result = query.first()
        if result:
            session['logged_in'] = True
        else:
            flash('wrong password!')
        return home()
    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def do_admin_signup():
    if request.method == 'POST':
        POST_USERNAME = str(request.form['username'])
        POST_PASSWORD = str(request.form['password'])

        result = db.session.query(User).filter(User.username.in_([POST_USERNAME])).first()
        if result:
            msg = 'Username already exists!'
            return render_template('signup.html', msg=msg)
        else:
            user = User(username=POST_USERNAME, password=POST_PASSWORD)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('do_admin_login'))
    else:
        return render_template('signup.html', msg='')


@app.route("/logout")
def logout():
    session['logged_in'] = False
    # return home()
    return redirect(url_for('do_admin_login'))


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=4000)
