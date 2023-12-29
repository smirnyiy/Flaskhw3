from string import ascii_lowercase
from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect

from .forms_7 import SingUpForm


app = Flask(__name__)
# Example secret key. REPLACE IT WITH REAL SECRET KEY
app.config['SECRET_KEY'] = 'secretkey'
csrf = CSRFProtect(app)


def validate_password(password: str) -> bool:
    has_letters = False
    has_digits = False
    for character in password.lower():
        if character in ascii_lowercase:
            has_letters = True
        if character.isdigit():
            has_digits = True

    if has_letters and has_digits:
        return True
    return False


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SingUpForm()
    form_notifications = []
    form_errors = []
    if request.method == 'POST' and form.validate():
        name = form.name.data
        last_name = form.last_name.data
        password = form.password.data
        if validate_password(password):
            form_notifications.append(
                f'User {name} {last_name} successfully registered!'
            )
        else:
            form.password.errors.append(
                'Password must contain at least one letter and one digit'
            )
    return render_template(
        '4.html',
        form=form,
        form_errors=form_errors,
        form_notifications=form_notifications,
    )


if __name__ == '__main__':
    app.run(debug=True)