from flask import Flask, jsonify, request
app = Flask(__name__)
products = {0:{'name': 'Product1', 'price':1000, 'quantity':5}}

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/products')
def get_all_products():
    return jsonify(products)
    
@app.route('/products/<int:_id>', methods=['GET'])
def get_product(_id):
    if _id not in products:
        return jsonify(success=False), 404
    return jsonify(products[_id])
    
@app.route('/products', methods=['POST'])
def create_product():
    #print(request.json)
    p = {'name':request.json.get('name'), 'price':request.json.get('price'), 'quantity':request.json.get('quantity')}
    products[max(products.keys()) + 1] = p
    return jsonify(p), 201

@app.route('/products/<int:_id>', methods=['PUT'])
def update_product(_id):
    if _id not in products:
        return jsonify(success=False), 404
    p = {'name':request.json.get('name'), 'price':request.json.get('price'), 'quantity':request.json.get('quantity')}
    products[_id] = p
    return jsonify(p)
    
@app.route('/products/<int:_id>', methods=['DELETE'])
def delete_product(_id):
    #print("hello")
    #print(products)
    if _id not in products:
        return jsonify(success=False), 404
        
    del(products[_id])
    return jsonify(success=True)