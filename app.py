# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from prettytable import prettytable

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_ASCII'] = False
db = SQLAlchemy(app)

INSTANCE = {
    "id": 19,
    "name": "test",
}
PUT = {"name": "Иванов Иван"}
PUTG = {"name": "horror"}

class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")

class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Str()
    genre_id = fields.Int()
    director_id = fields.Int()


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)

api = Api(app)
movie_ns = api.namespace('movies')
director_ns = api.namespace('director')
genre_ns = api.namespace('genres')


db.create_all()

@movie_ns.route('/')
class MovieView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')

        if director_id and genre_id:
            movies = Movie.query.filter_by(director_id=director_id, genre_id=genre_id).all()
        elif director_id:
            movies = Movie.query.filter_by(director_id=director_id).all()
        elif genre_id:
            movies = Movie.query.filter_by(genre_id=genre_id).all()
        else:
            movies = Movie.query.all()
        if movies:
            return movies_schema.dump(movies), 200, {'Content-Type': 'application/json; charset=utf-8'}

@movie_ns.route('/<int:uid>')
class MovieView(Resource):
    def get(self, uid: int):
        try:
            movie = Movie.query.get(uid)
            return movie_schema.dump(movie), 200
        except Exception as e:
            return "", 404

@director_ns.route('/')
class DirectorView(Resource):
    def get(self):
        directors = Director.query.all()
        return directors_schema.dump(directors), 200

    def post(self):
        new_director = Director(**request.json)
        with db.session.begin():
            db.session.add(new_director)
            db.session.commit()
        return "", 201

@director_ns.route('/<int:uid>')
class DirectorView(Resource):
    def put(self, uid: int):
        director = Director.query.get(uid)
        if not director:
            return "", 404
        director.name = request.json.get('name')
        db.session.add(director)
        db.session.commit()
        return "", 204

    def delete(self, uid: int):
        director = Director.query.get(uid)
        if not director:
            return "", 404
        db.session.delete(director)
        db.session.commit()
        return "", 204

@genre_ns.route('/')
class GenreView(Resource):
    def get(self):
        genres = Genre.query.all()
        return genres_schema.dump(genres), 200

    def post(self):
        new_genre = Genre(**request.json)
        with db.session.begin():
            db.session.add(new_genre)
            db.session.commit()
        return "", 201


@genre_ns.route('/<int:uid>')
class GenreView(Resource):
    def put(self, uid: int):
        genre = Genre.query.get(uid)
        if not genre:
            return "", 404
        genre.name = request.json.get('name')
        db.session.add(genre)
        db.session.commit()
        return "", 204

    def delete(self, uid: int):
        genre = Genre.query.get(uid)
        if not genre:
            return "", 404
        db.session.delete(genre)
        db.session.commit()
        return "", 204


if __name__ == '__main__':
    app.run()
#
# if __name__ == '__main__':
#     client = app.test_client()
#     # response = client.put('/director/1', json=PUT)
#     # response = client.delete('/director/5', json='')
#     # session = db.session()
#     # cursor = session.execute("SELECT * FROM director").cursor
#     response = client.put('/genre/1', json=PUTG)
#     # response = client.delete('/genre/5', json='')
#     response = client.post('/genre/', json='INSTANCE')
#     session = db.session()
#     cursor = session.execute("SELECT * FROM genre").cursor
#     mytable = prettytable.from_db_cursor(cursor)
#     mytable.max_width = 30
#     print("БАЗА ДАННЫХ")
#     print(mytable)