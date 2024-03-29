from product_list import app, db, Product
import json
import pytest

test_client = app.test_client()

# Add example item in the database
@pytest.fixture(scope='session', autouse=True)
def with_test_db():
    db.create_all()
    initial_product = Product(id=0, name='Product1', price=1000, quantity=5)

    db.session.add(initial_product)
    db.session.commit()
    
    yield
    
    db.drop_all()

def test_get_all_products():
    rv = test_client.get('/products')
    assert rv.status_code == 200
    assert rv.mimetype == 'application/json'
    
    assert len(rv.json) == 1
    
def test_get_product():
    rv = test_client.get('/products/0')
    assert rv.status_code == 200
    product = rv.json
    assert product['name'] == 'Product1'
    
def test_get_non_existing_product():
    rv = test_client.get('/products/100')
    assert rv.status_code == 404

def test_create_product():
    product = { 'name': 'Coffee', 'price': 16.99, 'quantity': 7}
    rv = test_client.post('/products', data=json.dumps(product), headers={'Content-Type': 'application/json'})
    
    assert rv.status_code == 201 # Created
    assert rv.json['name'] == 'Coffee'
    
def test_update_product():
    product = { 'name': 'Coffee', 'price': 23.00, 'quantity': 1}
    rv = test_client.put('/products/1', data=json.dumps(product), headers={'Content-Type': 'application/json'})
    assert rv.status_code == 200
    
    rv = test_client.get('/products/1')
    assert rv.json['quantity'] == 1
    assert rv.json['price'] == 23.00
    
def test_delete_product():
    rv = test_client.delete('/products/1')
    assert rv.status_code == 200
    
    rv = test_client.get('/products/1')
    assert rv.status_code == 404