from flask import Blueprint, jsonify, request
from models.address import Address
from services.address_service import AddressService

address_view = Blueprint('address_view', __name__)
address_service = AddressService()

@address_view.route('/addresses', methods=['GET'])
def get_addresses():
    addresses = address_service.get_addresses()
    return jsonify(addresses)

@address_view.route('/addresses', methods=['POST'])
def create_address():
    data = request.get_json()
    country = data.get('country')
    city = data.get('city')
    city_image = data.get('city_image')
    district = data.get('district')
    district_image = data.get('district_image')
    coordinates = data.get('coordinates')
    coordinates_image = data.get('coordinates_image')

    address = Address(country=country, city=city, city_image=city_image,
                      district=district, district_image=district_image,
                      coordinates=coordinates, coordinates_image=coordinates_image)
    created_address = address_service.create_address(address)
    return jsonify({'message': 'Address created successfully', 'address': created_address})

@address_view.route('/addresses/<int:address_id>', methods=['GET'])
def get_address(address_id):
    address = address_service.get_address(address_id)
    if address:
        return jsonify(address)
    else:
        return jsonify({'message': 'Address not found'}), 404

@address_view.route('/addresses/<int:address_id>', methods=['PUT'])
def update_address(address_id):
    data = request.get_json()
    updated_address = address_service.update_address(address_id, data)
    if updated_address:
        return jsonify({'message': 'Address updated successfully', 'address': updated_address})
    else:
        return jsonify({'message': 'Address not found'}), 404

@address_view.route('/addresses/<int:address_id>', methods=['DELETE'])
def delete_address(address_id):
    result = address_service.delete_address(address_id)
    if result:
        return jsonify({'message': 'Address deleted successfully'})
    else:
        return jsonify({'message': 'Address not found'}), 404
