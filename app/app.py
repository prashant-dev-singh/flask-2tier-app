import time
from flask import Flask, render_template, request, redirect
from models import db, User
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# ✅ SIMPLE DB INIT (works everywhere)
with app.app_context():
    db.create_all()


# ✅ NEW WAY (Flask 3 compatible)
with app.app_context():
    db.create_all()

@app.route('/')
def index():   
   return render_template('index.html')
 #return "Flask is working 🚀"

@app.route('/users')
def users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users)

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()
        return redirect('/users')
    return render_template('add_user.html')

@app.route('/delete/<int:id>')
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect('/users')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    user = User.query.get_or_404(id)

    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        db.session.commit()
        return redirect('/users')
    return render_template('edit_user.html', user=user)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
