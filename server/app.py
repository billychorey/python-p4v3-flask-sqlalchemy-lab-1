# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from models import db, Earthquake
from sqlalchemy.orm import Session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# New view to get an earthquake by ID
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    session = Session(db.engine)
    earthquake = session.get(Earthquake, id)
    if earthquake:
        response = {
            'id': earthquake.id,
            'location': earthquake.location,
            'magnitude': earthquake.magnitude,
            'year': earthquake.year
        }
        return jsonify(response), 200
    else:
        response = {'message': f'Earthquake {id} not found.'}
        return jsonify(response), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)
