from flask import Flask, jsonify, abort, request, render_template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)

class Videogame(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    titulo = db.Column(db.String(120), nullable=False)  
    desarrollador = db.Column(db.String(120), nullable=False)  
    anio_de_lanzamiento = db.Column(db.String(4), nullable=False)  
    plataforma = db.Column(db.String(120), nullable=False)
    clasificacion = db.Column(db.String(120), nullable=False)

    def videogames_bd(self):
        return {
            'id': self.id,
            'name': self.titulo,
            'category': self.desarrollador,
            'status': self.anio_de_lanzamiento,
            'created': self.plataforma,
            'update': self.clasificacion
        }

BASE_URL = '/api/'

@app.route('/')
def home():
    return 'Welcome to my api'

@app.route(BASE_URL + 'videogames', methods=['POST'])
def create_videogame():
    if not request.json:
        abort(400, "Missing JSON body in request")
    if 'titulo' not in request.json:
        abort(400, "Error, missing 'titulo' in JSON data.")
    if 'desarrollador' not in request.json:
        abort(400, "Error, missing 'desarrollador' in JSON data.")
    if 'anio_de_lanzamiento' not in request.json:
        abort(400, "Error, missing 'anio_de_lanzamiento' in JSON data.")
    if 'plataforma' not in request.json:
        abort(400, "Error, missing 'plataforma' in JSON data.")
    if 'clasificacion' not in request.json:
        abort(400, "Error, missing 'clasificacion' in JSON data.")
    videogame = Videogame(titulo=request.json['titulo'], desarrollador=request.json['desarrollador'], anio_de_lanzamiento=request.json['anio_de_lanzamiento'], plataforma=request.json['plataforma'], clasificacion=request.json['clasificacion'])
    db.session.add(videogame)  
    db.session.commit() 
    return jsonify({'videogame': videogame.videogames_bd()}), 201 

@app.route(BASE_URL +'videogames', methods=['GET'])
def get_videogames():
    videogames = Videogame.query.all()  
    return jsonify({'videogames': [videogame.videogames_bd() for videogame in videogames]}) 



@app.route(BASE_URL + 'videogames/<int:id>', methods=['GET'])
def get_videogame(id):
    videogame = Videogame.query.get(id) 
    if videogame is None:
        return jsonify({'error': 'Videogame not found'}), 404
    return jsonify({'videogame': videogame.videogames_bd()})

@app.route(BASE_URL + 'videogames/<int:id>', methods=['PUT'])
def update_videogame(id):
    videogame = Videogame.query.get(id)
    if videogame is None:
        return jsonify({'error': 'Videogame not found'}), 404
    if not request.json:
        abort(400, "Missing JSON body in request")
    videogame.titulo = request.json.get('titulo', videogame.titulo)
    videogame.desarrollador = request.json.get('desarrollador', videogame.desarrollador)
    videogame.anio_de_lanzamiento = request.json.get('anio_de_lanzamiento', videogame.anio_de_lanzamiento)
    videogame.plataforma = request.json.get('plataforma', videogame.plataforma)
    videogame.clasificacion = request.json.get('clasificacion', videogame.clasificacion)
    db.session.commit()
    return jsonify({'videogame': videogame.videogames_bd()})

#
@app.route(BASE_URL + 'videogames/<int:id>', methods=['DELETE'])
def delete_videogame(id):
    videogame = Videogame.query.get(id)
    if videogame is None:
        return jsonify({'error': 'Videogame not found'}), 404
    db.session.delete(videogame)  
    db.session.commit()  
    return jsonify({'result': True})  


if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)