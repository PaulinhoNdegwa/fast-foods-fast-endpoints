"""import modules"""
import re
from flask import jsonify, abort, request
from fastfoodsfast import APP
from fastfoodsfast.models.auth import User, USERS
from fastfoodsfast.models.foods import Fooditem, FOODITEMS, Order,ORDERS

email_format = r"(^[a-zA-z0-9_.]+@[a-zA-z0-9-]+\.[a-z]+$)"


@APP.route('/api/v1', methods=['GET'])
def index():
    """Function to handle index page"""
    return jsonify({"message": "Hello, welcome to Fast-foods-fast"})


@APP.route('/api/v1/auth/signup', methods=['POST'])
def signup():
    """signup function"""
    email = request.get_json('email')['email'].strip(" ")
    password = request.get_json('password')['password'].strip(" ")
    if not email or email == '':
        response = jsonify({"message": "Please enter an email"})
        response.status_code = 400
        return response
    if not re.match(email_format, email):
        response = jsonify({"message": "Please use a valid email format"})
        response.status_code = 400
        return response
    if not password or password == '':
        response = jsonify({"message": "Please enter a password"})
        response.status_code = 400
        return response
    if not request.json:
        response = jsonify({"message": "Invalid format"})
        response.status_code = 400
        return response
    
    existing_email = [user for user in USERS if user['email'] == email]
    if existing_email:
        response = jsonify({"message": "Email already exists"})
        response.status_code = 409
        return response
    user = User(str(email), str(password))
    USERS.append(user.__dict__)
    new_user = [user for user in USERS if user['email'] == email]
    return jsonify({"User": new_user[0]})


@APP.route('/api/v1/auth/signin', methods=['POST'])
def signin():
    """Signin function"""
    email = request.get_json('email')['email'].strip(" ")
    password = request.get_json('password')['password'].strip(" ")

    if not email or email == '':
        response = jsonify({"message": "Please enter an email"})
        response.status_code = 400
        return response
    if not re.match(email_format, email):
        response = jsonify({"message": "Please use a valid email format"})
        response.status_code = 400
        return response
    if not password or password == '':
        response = jsonify({"message": "Please enter a password"})
        response.status_code = 400
        return response
    if not request.json:
        response = jsonify({"message": "Invalid format"})
        response.status_code = 400
        return response
    user_exists = [user for user in USERS if user['email'] == email]
    # print(user_exists)
    if not user_exists:
        response = jsonify({"message": "User does not exist"})
        response.status_code = 404
        return response
    user_password = user_exists[0]['password']
    # print(user_password)
    if password != user_password:
        response = jsonify({"message": "Incorrect password"})
        response.status_code = 400
        return response

    return jsonify({"User logged in: ": email})

@APP.route("/api/v1/fooditem", methods=['POST'])
def newfooditem():
    """New footitem function"""
    name = request.get_json("name")["name"].strip(" ")
    price = request.get_json("price")["price"].strip(" ")
    imagesrc = request.get_json("imagesrc")["imagesrc"].strip(" ")

    if not name or len(name) == 0:
        response = jsonify({"message": "Please enter an fooditem name"})
        response.status_code = 400
        return response
    if not price or len(price) == 0:
        response = jsonify({"message": "Please enter an fooditem price"})
        response.status_code = 400
        return response
    if not request.json:
        response = jsonify({"message": "Invalid input format"})
        response.status_code = 400
        return response

    food_exists = [fooditem for fooditem in FOODITEMS if fooditem["name"] == name]
    if food_exists:
        response = jsonify({"message": "Food item already exists"})
        response.status_code = 409
        return response

    fooditem = Fooditem(name, price, imagesrc)
    FOODITEMS.append(fooditem.__dict__)
    new_fooditem = [fooditem for fooditem in FOODITEMS if fooditem["name"] == name]
    return jsonify({"Fooditem : ": new_fooditem})

@APP.route('/api/v1/orders', methods=["POST", "GET"])
def neworder():
    if request.method == 'POST':
        fooditem = request.get_json("fooditem")["fooditem"].strip(" ")
        customer_email = request.get_json("customer")["customer"].strip(" ")

        if not fooditem or len(fooditem) == 0:
            response = jsonify({"message": "Please select food item to order"})
            response.status_code = 400
            return response

        if not customer_email or len(customer_email) == 0:
            # response = jsonify({"message": "Please enter customer"})
            # response.status_code = 400
            abort(400)
        
        customer_exists = [user for user in USERS if user['email'] == customer_email]
        if not customer_exists:
            response = jsonify({"message": "Customer does not exist. Please register"})
            response.status_code = 400
            return response
            
        if not request.json:
            response = jsonify({"message": "Invalid input format"})
            response.status_code = 400
            return response

        food_exists = [item for item in FOODITEMS if item["name"] == fooditem]
        if not food_exists:
            response = jsonify({"message": "Food item does not exist"})
            response.status_code = 404
            return response

        price = food_exists[0]['price']
        order = Order(str(customer_email),str(fooditem),price)
        ORDERS.append(order.__dict__)
        return jsonify({"Order :": ORDERS[-1]})
    
    return jsonify({"Orders":ORDERS})


@APP.route('/api/v1/orders/<order_id>', methods=['GET', "PUT"])
def order(order_id):
    if not order_id:
        abort(400, "Please select order to display")

    order_exist  = [order for order in ORDERS if order["order_id"] == order_id]
    if len(order_exist)==0:
        return jsonify({"message":"Order does not exist"})
    if request.method == 'GET':
        return jsonify({"Order: ": order_exist})

    new_status = request.get_json('new_status')['new_status'].strip(" ")
    order_exist[0]['status']= new_status
    return jsonify({"Updated order": order_exist})
        

    