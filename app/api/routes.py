from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, car_schema, cars_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata', methods=['GET'])
def getdata():
    return {'some':'JSON'}

@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    name = request.json['name']
    description = request.json['description']
    phone_number = request.json['phone_number']
    address = request.json['address']
    price = request.json['price']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    car = Car(name, description, phone_number, address,price, user_token = user_token )

    db.session.add(car)     
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/cars', methods = ['GET'])
@token_required
def get_contact(current_user_token):
    a_user = current_user_token.token
    cars = Car.query.filter_by(user_token = a_user).all()
    response = cars_schema.dump(cars)
    return jsonify(response)    


@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_single_contact(current_user_token, id):
    car = Car.query.get(id)
    response = car_schema.dump(car)
    return jsonify(response) 

@api.route('/cars/<id>', methods = ['POST','PUT'])
@token_required
def update_contact(current_user_token,id):
    car = Car.query.get(id) 
    car.name = request.json['name']
    car.description = request.json['description']
    car.phone_number = request.json['phone_number']
    car.address = request.json['address']
    car.price = request.json['price']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)  


@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_contact(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)        