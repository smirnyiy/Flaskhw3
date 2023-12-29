from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect

from .forms_4 import SingUpForm
from .models_4 import db, User


app = Flask(__name__)
# Example secret key. REPLACE IT WITH REAL SECRET KEY
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///4.sqlite'
db.init_app(app)
csrf = CSRFProtect(app)


def add_user(username, email, password):
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SingUpForm()
    form_errors = []
    if request.method == 'POST' and form.validate():
        username = form.name.data
        email = form.email.data
        if User.query.filter(User.username == username).count() > 0:
            form_errors.append(f'Username {username} already taken!')
        if User.query.filter(User.email == email).count() > 0:
            form_errors.append(f'Email {email} already taken!')
        else:
            print(f'Adding user {username}!')
            add_user(username, form.email.data, form.password.data)
            form_notifications = [f'User {username} successfully registered!']
            return render_template(
                '4.html', form=form, form_notifications=form_notifications
            )
    return render_template('4.html', form=form, form_errors=form_errors)


@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('Database created successfully!')


if __name__ == '__main__':
    app.run(debug=True)