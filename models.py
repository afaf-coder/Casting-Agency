import os
from sqlalchemy import Column, String, Integer, Date, create_engine
from flask_sqlalchemy import SQLAlchemy
import json


DATABASE_URI = 'postgres://aryggjifcqwmur:7cadc855538c0840ca9e79202056e899d3f1f0861543127a57dfd81807a1f64b@ec2-52-44-46-66.compute-1.amazonaws.com:5432/dep76g3od832hk'

db = SQLAlchemy()


def setup_db(app, database_path=DATABASE_URI):
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()



# Movies with attributes title and release date

class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
        }

# Actors with attributes name, age and gender
class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    movies = db.relationship('Movie', secondary='ActorsMovies',
                             backref=db.backref('actors', lazy='dynamic'))

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }

    actors_movies = db.Table(
        'ActorsMovies',
        db.Column('actor_id', db.Integer, db.ForeignKey('Actor.id'), primary_key=True),
        db.Column('movie_id', db.Integer, db.ForeignKey('Movie.id'), primary_key=True),
    )
