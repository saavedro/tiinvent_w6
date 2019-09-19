from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", default="sqlite:///test.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),  nullable=False)
    price = db.Column(db.Float())
    quantity = db.Column(db.Float())

    def serialize(self):
        return {'id': self.id, 'name': self.name, 'price': self.price, 'quantity': self.quantity}

#products = {0:{'name': 'Product1', 'price':1000, 'quantity':5}}

@app.route('/createdb')
def create_db():
    db.create_all()
    return jsonify(success=True), 201
    
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/products')
def get_all_products():
    return jsonify(json_list=[p.serialize() for p in Product.query.all()])
    
@app.route('/products/<int:_id>', methods=['GET'])
def get_product(_id):
    product = Product.query.get(_id)
    if not product:
        return jsonify(success=False), 404
    return jsonify(product.serialize())
    
@app.route('/products', methods=['POST'])
def create_product():
    #print(request.json)
    p = {'name':request.json.get('name'), 'price':request.json.get('price'), 'quantity':request.json.get('quantity')}
    product = Product(**p)
    db.session.add(product)
    db.session.commit()
    return jsonify(product.serialize()), 201

@app.route('/products/<int:_id>', methods=['PUT'])
def update_product(_id):
    product = Product.query.get(_id)
    if not product:
        return jsonify(success=False), 404
    product.name = request.json.get('name')
    product.price = request.json.get('price')
    product.quantity = request.json.get('quantity')
    db.session.add(product)
    db.session.commit()
    return jsonify(product.serialize())
    
@app.route('/products/<int:_id>', methods=['DELETE'])
def delete_product(_id):
    product = Product.query.get(_id)
    if not product:
        return jsonify(success=False), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify(success=True)
