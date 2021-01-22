import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie
from auth import AuthError, requires_auth


def create_app(test_config=None):
    app = Flask(__name__)
    app.debug = True
    CORS(app)
    setup_db("my_schema")

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def home():
        return jsonify({
            'success': True
        })

    # GET actors
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        try:
            actors = Actor.query.order_by(Actor.id).all()
            formatted_actors = [actor.format() for actor in
                                actors]

            return jsonify({'success': True,
                            "status_code": 200,
                            'actors': formatted_actors})
        except:
            abort(422)

    # GET movies
    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        try:
            movies = Movie.query.order_by(Movie.id).all()
            formatted_movies = [movie.format() for movie in
                                movies]

            return jsonify({'success': True,
                            "status_code": 200,
                            'movies': formatted_movies})
        except:
            abort(422)

    # DELETE actor by actor id
    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, id):
        actor = Actor.query.get(id)
        if actor == None:
            abort(404)
        actor.delete()
        return jsonify({
            'success': True,
            "status_code": 200,
            'deleted': id
        })

    # DELETE movie by movie id
    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, id):
        movie = Movie.query.get(id)
        if movie == None:
            abort(404)
        movie.delete()
        return jsonify({
            'success': True,
            "status_code": 200,
            'deleted': id
        })

    # POST actors
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        data = []
        body = request.get_json()
        if 'name' not in body or 'age' not in body or 'gender' not in body:
            abort(400)

        if 'name' == None or 'age' == None or 'gender' == None:
            abort(422)

        try:
            name = body['name']
            age = body['age']
            gender = body['gender']
            new_actor = Actor(name=name, age=age, gender=gender)
            new_actor.insert()
            return jsonify({
                'success': True,
                'create': new_actor.format()
            }), 201
        except:
            abort(422)

    # POST movie
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        body = request.get_json()
        if 'title' not in body or 'release_date' not in body:
            abort(422)

        if 'title' == None or 'release_date' == None:
            abort(400)

        try:
            title = body['title']
            release_date = body['release_date']
            new_movie = Movie(title=title, release_date=release_date)
            new_movie.insert()
            return jsonify({
                'success': True,
                'create': new_movie.format()
            }), 201
        except:
            abort(422)

    # PATCH actors by actor id
    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, id):
        body = request.get_json()
        name = body.json.get("name", None)
        age = body.json.get("age", None)
        gender = body.json.get("gender", None)
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if actor == None:
            abort(404)

        try:
            actor.name = name
            actor.age = age
            actor.gender = gender
            actor.update()

            return jsonify({
                'success': True,
                'updated': actor.format()
            }), 200

        except:
            abort(422)

    # PATCH movie by movie id
    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, id):
        body = request.get_json()
        title = body.json.get("title", None)
        release_date = body.json.get("release_date", None)
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if movie == None:
            abort(404)

        try:
            movie.title = title
            movie.release_date = release_date
            movie.update()

            return jsonify({
                'success': True,
                'updated': movie.format()
            }), 200

        except:
            abort(422)

    # Error Handling
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": 'Unathorized'
        }), 401

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
