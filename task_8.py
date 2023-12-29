import os
from hashlib import pbkdf2_hmac
from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect

from .forms_7 import SingUpForm


app = Flask(__name__)
# Example secret key. REPLACE IT WITH REAL SECRET KEY
app.config['SECRET_KEY'] = 'secretkey'
csrf = CSRFProtect(app)

# Database example to avoid using databases in all of the tasks
EXAMPLE_DB = {}


def hash_password(password: str) -> bytes:
    salt = os.urandom(32)
    key = pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100_000)
    hashed_password = salt + key
    return hashed_password


def check_password(password: str, hashed_password: bytes) -> bool:
    stored_salt, stored_key = hashed_password[:32], hashed_password[32:]
    new_key = pbkdf2_hmac(
        'sha256', password.encode('utf-8'), stored_salt, 100_000
    )
    return new_key == stored_key


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SingUpForm()
    form_notifications = []
    if request.method == 'POST' and form.validate():
        name = form.name.data
        password = form.password.data
        EXAMPLE_DB[name] = {
            field.name: field.data
            for field in form
            if field.name not in ('name', 'password')
        }
        hashed_password = hash_password(password)
        print(f'{password = }')
        print(f'{hashed_password = }')
        print(f'{check_password(password, hashed_password) = }')
        EXAMPLE_DB[name]['password'] = hashed_password
        form_notifications.append('User registered, password hashed!')

    return render_template(
        '4.html',
        form=form,
        form_notifications=form_notifications,
    )


if __name__ == '__main__':
    app.run(debug=True)