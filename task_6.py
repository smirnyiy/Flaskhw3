from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect

from .forms_6 import SingUpForm


app = Flask(__name__)
# Example secret key. REPLACE IT WITH REAL SECRET KEY
app.config['SECRET_KEY'] = 'secretkey'
csrf = CSRFProtect(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SingUpForm()
    form_notifications = []
    if request.method == 'POST' and form.validate():
        username = form.name.data
        email = form.email.data
        form_notifications.append(
            f'User {username}({email}) successfully registered!'
        )
        return render_template(
            '4.html', form=form, form_notifications=form_notifications
        )
    return render_template('4.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)