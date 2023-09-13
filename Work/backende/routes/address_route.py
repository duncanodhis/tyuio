from flask import Blueprint, jsonify, request,current_app
from models.address import Address
from services.address_service import AddressService
import os
from flask import send_file
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity
)
address_routes = Blueprint('address_routes', __name__)
address_service = AddressService()
# Initialize JWT manager
jwt = JWTManager()

@address_routes.route('/api/addresses', methods=['GET'])
def get_addresses():
    addresses = address_service.get_addresses()
    return jsonify(addresses)

@address_routes.route('/api/addresses', methods=['POST'])
def create_address():
    upload_folder = current_app.config['UPLOAD_FOLDER']
    if 'cityImage' not in request.files or 'districtImage' not in request.files:
        return jsonify({'error': 'Both cityImage and districtImage must be provided.'}), 400
    
    country = request.form.get('country')
    city = request.form.get('city')
    district = request.form.get('district')
    city_image = request.files['cityImage']
    district_image = request.files['districtImage']
    # print(country,city,district)
    
    city_image.save(os.path.join(upload_folder, city_image.filename))
    district_image.save(os.path.join(upload_folder, district_image.filename))
   
    city_image_path = os.path.join(upload_folder, city_image.filename)
    district_image_path = os.path.join(upload_folder, district_image.filename)

    
    # print(city_image_path)
    address_data = {
        'country': country,
        'city': city,
        'city_image': city_image_path,
        'district': district,
        'district_image': district_image_path,
    }
    # print("here")
    created_address = address_service.create_address(address_data)
    return jsonify({'message': 'Address created successfully', 'address': created_address})

@address_routes.route('/api/addresses/<int:address_id>', methods=['GET'])
def get_address(address_id):
    address = address_service.get_address(address_id)
    if address:
        return jsonify(address)
    else:
        return jsonify({'message': 'Address not found'}), 404

@address_routes.route('/api/addresses/<int:address_id>', methods=['PUT'])
def update_address(address_id):
    data = request.get_json()
    updated_address = address_service.update_address(address_id, data)
    if updated_address:
        return jsonify({'message': 'Address updated successfully', 'address': updated_address})
    else:
        return jsonify({'message': 'Address not found'}), 404

@address_routes.route('/api/addresses/<int:address_id>', methods=['DELETE'])
def delete_address(address_id):
    result = address_service.delete_address(address_id)
    if result:
        return jsonify({'message': 'Address deleted successfully'})
    else:
        return jsonify({'message': 'Address not found'}), 404

@address_routes.route('/api/addresses/countries', methods=['GET'])
def get_countries():
    countries = address_service.get_countries()
    return jsonify(countries)

@address_routes.route('/api/countries/<string:country>/cities', methods=['GET'])
def get_cities_in_country(country):
    cities = address_service.get_cities_in_country(country)
    return jsonify(cities)

@address_routes.route('/api/countries/<string:country>/cities/<string:city>/districts', methods=['GET'])
def get_districts_in_city(country, city):
    districts = address_service.get_districts_in_city(country, city)
    return jsonify(districts)


@address_routes.route('/api/countries/<string:country>/cities/<string:city>/photo', methods=['GET'])
def get_city_photo(country, city):
    # Retrieve city photo path based on country and city
    city_photo_path = address_service.get_city_photo_path(country, city)
    print(city_photo_path)
    if city_photo_path:
        # Return the image file as a response
        return send_file(city_photo_path, mimetype='image/jpeg')
    else:
        return jsonify({'message': 'City photo not found'}), 404

@address_routes.route('/api/countries/<string:country>/cities/<string:city>/districts/<string:district>/photo', methods=['GET'])
def get_district_photo(country, city, district):
    # Retrieve district photo path based on country, city, and district
    district_photo_path = address_service.get_district_photo_path(country, city, district)
    print(district_photo_path)
    if district_photo_path:
        # Return the image file as a response
        return send_file(district_photo_path, mimetype='image/jpeg')
    else:
        return jsonify({'message': 'District photo not found'}), 404


@address_routes.route('/api/countries/<string:selected_country>/cities/<string:selected_city>/<string:selected_district>', methods=['GET'])
def get_address_by_location(selected_country, selected_city, selected_district):
    address = address_service.get_address_by_location(selected_country, selected_city, selected_district)
    
    if address:
        return jsonify(address)
    else:
        return jsonify({'message': 'Address not found'}), 404
