from faker import Faker
from flask import Flask, render_template
from random import choice, randint

from .models_3 import db, Student, Grade


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///3.sqlite'
db.init_app(app)
fake = Faker('ru-RU')


@app.route('/')
def index():
    students = Student.query.all()
    context = {'students': students}
    return render_template('3.html', **context)


@app.cli.command('init-db')
def init_db():
    db.create_all()
    print('Database created successfully!')


@app.cli.command('fill-db')
def fill_db():
    disciplines = [
        'Математика',
        'Физика',
        'Прикладное программирование',
        'Базы данных',
        'Информационные системы',
    ]
    groups = ['ПИН-20-1', 'ИнБ-20-1']
    for _ in range(10):
        student = Student(
            name=fake.first_name(),
            last_name=fake.last_name(),
            group=choice(groups),
            email=fake.safe_email(),
        )
        db.session.add(student)
        print(f'Created student: {student}')

        for _ in range(20):
            grade = Grade(
                student=student,
                discipline_name=choice(disciplines),
                grade=randint(2, 5),
            )
            db.session.add(grade)

        print(f'Filled grades for student: {student}')

    db.session.commit()
    print('Database filled successfully!')


if __name__ == '__main__':
    app.run(debug=True)