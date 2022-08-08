from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')

db = SQLAlchemy(app)


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created!')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped')


@app.cli.command('db_seed')
def db_seed():
    mercury = Planet(planet_name='Mercury',
                     planet_type='Class D',
                     home_star='Sol',
                     mass=3.258,
                     radius=1516,
                     distance=35.98e6)
    venus = Planet(planet_name='venus',
                   planet_type='Class K',
                   home_star='Sol',
                   mass=4.868e6,
                   radius=3760,
                   distance=67.98e6)
    earth = Planet(planet_name='Earth',
                   planet_type='Class M',
                   home_star='Sol',
                   mass=5.958e24,
                   radius=3959,
                   distance=92.98e6)
    db.session.add(mercury)
    db.session.add(venus)
    db.session.add(earth)

    test_user = User(first_name='Syed',
                     last_name='Ayaz',
                     email='test@test.com',
                     password='Passwod@')

    db.session.add(test_user)
    db.session.commit()
    print('Database seeded')


@app.route('/')  # end point
def hello_world():
    return 'hello test'


@app.route('/super_simple')
def super_simple():
    return jsonify(
        message='Hello from the Planetary API'), 200  # Some people like hardcode of respose but It is by default.


@app.route('/not_found')
def not_found():
    return jsonify(message="That resource was not found"), 404


@app.route('/parameters')
def parameters():
    name = request.args.get('name')
    age = int(request.args.get('age'))
    if age < 18:
        return jsonify(message="Sorry " + name + " You are not old enough"), 401
    else:
        return jsonify(message="Welcome " + name + " you are old enough")


# url_variable/alice/27
@app.route('/url_variable/<string:name>/<int:age>')
def url_variable(name: str, age: int):
    if age < 18:
        return jsonify(message="Sorry " + name + " You are not old enough"), 401
    else:
        return jsonify(message="Welcome " + name + " you are old enough")


# database models
class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


class Planet(db.Model):
    __table_name = 'planets'
    planet_id = Column(Integer, primary_key=True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    radius = Column(Float)
    distance = Column(Float)


if __name__ == '__main__':
    app.run()
