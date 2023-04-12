from flask import Flask, jsonify, request
from models import db, User, Product, Cart
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Apply CORS settings to the Flask app

@app.after_request
def add_cors_headers(response):
    # Add CORS headers to the response
    response.headers.add('Access-Control-Allow-Origin', '*') # Allow requests from any origin
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization') # Allow specific headers
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE') # Allow specific HTTP methods
    return response

# Configure the database connection settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Define your routes
# Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(name=data['name'],
                email=data['email'],
                password=data['password'],
                profile=data['profile'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

# Get a user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({'error': 'User not found'}), 404

# Update a user by ID
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if user:
        data = request.get_json()
        user.name = data['name']
        user.email = data['email']
        user.password = data['password']
        user.profile = data['profile']
        user.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({'error': 'User not found'}), 404

# Delete a user by ID
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

# Create a new product
@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    product = Product(product_name=data['product_name'],
                      descr=data['descr'],
                      quantity=data['quantity'],
                      price=data['price'],
                      category=data['category'],
                      image1=data['image1'],
                      image2=data['image2'],
                      user_id=data['user_id'])
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201

# Get all products
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products]), 200

# Get a product by ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify(product.to_dict()), 200
    else:
        return jsonify({'error': 'Product not found'}), 404


@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    # Get the product by its id
    product = Product.query.get(product_id)

    # Check if the product exists
    if product is None:
        return jsonify({'error': 'Product not found'}), 404

    # Update the product with the new data from the request
    product.product_name = request.form.get('product_name', product.product_name)
    product.descr = request.form.get('descr', product.descr)
    product.quantity = request.form.get('quantity', product.quantity)
    product.price = request.form.get('price', product.price)
    product.category = request.form.get('category', product.category)
    product.image1 = request.form.get('image1', product.image1)
    product.image2 = request.form.get('image2', product.image2)

    # Commit the changes to the database
    db.session.commit()

    # Return the updated product as JSON response
    return jsonify({'product': product.to_dict()}), 200


@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    # Get the user_id and product_id from the request
    user_id = request.form.get('user_id')
    product_id = request.form.get('product_id')

    # Check if user_id and product_id are provided
    if not user_id or not product_id:
        return jsonify({'error': 'User ID and Product ID are required'}), 400

    # Check if the user and product exist in the database
    user = User.query.get(user_id)
    product = Product.query.get(product_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    if not product:
        return jsonify({'error': 'Product not found'}), 404

    # Create a new cart item
    cart_item = Cart(
        descr=product.descr,
        quantity=1,
        price=product.price,
        category=product.category,
        image1=product.image1,
        image2=product.image2,
        product_id=product.id,
        user_id=user.id
    )

    # Add the cart item to the database
    db.session.add(cart_item)
    db.session.commit()

    # Return the cart item as a JSON response
    return jsonify({'message': 'Product added to cart successfully', 'cart_item': cart_item.to_dict()}), 201


@app.route('/cart/remove', methods=['POST'])
def remove_from_cart():
    # Get the user_id and product_id from the request
    user_id = request.form.get('user_id')
    product_id = request.form.get('product_id')

    # Check if user_id and product_id are provided
    if not user_id or not product_id:
        return jsonify({'error': 'User ID and Product ID are required'}), 400

    # Check if the user and product exist in the database
    user = User.query.get(user_id)
    product = Product.query.get(product_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    if not product:
        return jsonify({'error': 'Product not found'}), 404

    # Find the cart item associated with the user and product
    cart_item = Cart.query.filter_by(user_id=user.id, product_id=product.id).first()

    if not cart_item:
        return jsonify({'error': 'Product not found in cart'}), 404

    # Remove the cart item from the database
    db.session.delete(cart_item)
    db.session.commit()

    # Return success message as a JSON response
    return jsonify({'message': 'Product removed from cart successfully'}), 200


if __name__ == '__main__':
    with app.app_context():  
        db.create_all()  
    app.run(debug=True)
