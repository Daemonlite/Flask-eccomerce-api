from flask import Flask, jsonify, request
from models import db, User, Product,Cart
from flask_cors import CORS



app = Flask(__name__)
CORS(app)  # Apply CORS settings to the Flask app

@app.after_request
def add_cors_headers(response):
    # Add CORS headers to the response
    response.headers.add('Access-Control-Allow-Origin', '*') # Allow requests from this origin
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization') # Allow specific headers
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE') # Allow specific HTTP methods
    return response
# Configure the database connection settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Define your routes

@app.route('/users', methods=["GET"])
def get_users():
    users = User.query.all()
    user_list = [user.to_dict() for user in users]
    return jsonify(users=user_list)

@app.route('/user/<int:user_id>', methods=["GET"])
def user_profile(user_id):
    profile = User.query.get(user_id)
    if profile:
        return jsonify(profile.to_dict())
    else:
        return jsonify({'error': 'Profile not found.'}), 404

@app.route('/register', methods=["POST"])
def register_user():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    profile = request.json['profile']
    new_user = User(name=name, email=email, password=password,profile=profile)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully.', 'user': new_user.to_dict()}), 201

@app.route('/login', methods=["POST"])
def login():
    email = request.json['email']
    password = request.json['password']
    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        return jsonify({'message': 'Login successful.', 'user': user.to_dict()})
    else:
        return jsonify({'error': 'Invalid email or password.'}), 401

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'user deleted successfully.'})
    else:
        return jsonify({'error': 'user not found.'}), 404
    

@app.route('/products',methods=["GET"])
def getProducts():
    products = Product.query.all()
    prod_list = [prod.to_dict() for prod in products]
    return jsonify(products=prod_list)


@app.route('/products/<int:prod_id>',methods=["GET"])
def get_product_by_id(prod_id):
    prods = Product.query.get(prod_id)
    if prods:
        return jsonify(prods.to_dict())
    else:
        return jsonify({'error': 'Product not found.'}), 404

@app.route('/product/create',methods=["GET"])
def create_product():
    # Get data from request
    product_name = request.json['product']
    descr = request.json['descr']
    quantity = request.json['quantity']
    price = request.json['price']
    category = request.json['category']
    image1 = request.json['image1']
    image2 = request.json['image2']
    user_id = request.json['user_id']


    # Check if all required data is provided
    if product_name and descr and user_id and quantity and price and category and image1 and image2:
        try:
            # Create a new product object
            product = Product(product_name=product_name, quantity=quantity, price=price, image1=image1, image2=image2 ,user_id=user_id)

            # Add and commit the new product to the database
            db.session.add(product)
            db.session.commit()

            # Return success response
            return jsonify({'message': 'product created successfully', 'product_id': product.id}), 201
        except Exception as e:
            # Return error response if an error occurs
            db.session.rollback()
            return jsonify({'message': 'Failed to create product', 'error': str(e)}), 500
    else:
        # Return error response if required data is missing
        return jsonify({'message': 'Missing required data'}), 400
