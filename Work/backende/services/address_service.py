from models.address import Address
from app import db

class AddressService:
    def get_addresses(self):
        addresses = Address.query.all()
        return [self._convert_to_dict(address) for address in addresses]

    def get_address(self, address_id):
        address = Address.query.get(address_id)
        return self._convert_to_dict(address) if address else None

    def create_address(self, data):
        address = Address(**data)
        db.session.add(address)
        db.session.commit()
        return self._convert_to_dict(address)

    def update_address(self, address_id, data):
        address = Address.query.get(address_id)
        if address:
            for key, value in data.items():
                setattr(address, key, value)
            db.session.commit()
            return self._convert_to_dict(address)
        return None

    def delete_address(self, address_id):
        address = Address.query.get(address_id)
        if address:
            db.session.delete(address)
            db.session.commit()
            return True
        return False
    
    def get_countries(self):
        countries = Address.query.with_entities(Address.country).distinct().all()
        return [country[0] for country in countries]
    
    def _convert_to_dict(self, address):
        if address:
            return {key: getattr(address, key) for key in address.__dict__.keys() if not key.startswith('_')}
        return None

    def get_cities_in_country(self, country):
        # Query distinct cities in the given country
        cities = Address.query.filter_by(country=country).with_entities(Address.city).distinct().all()
        return [city[0] for city in cities]

    def get_districts_in_city(self, country, city):
        # Query districts in the given city within the country
        districts = Address.query.filter_by(country=country, city=city).with_entities(Address.district).distinct().all()
        return [district[0] for district in districts]
    
    def get_city_photo_path(self, country, city):
        # Query the database to get the city photo path
        address = Address.query.filter_by(country=country, city=city).first()
        if address:
            return address.city_image
        return None

    def get_district_photo_path(self, country, city, district):
        # Query the database to get the district photo path
        address = Address.query.filter_by(country=country, city=city, district=district).first()
        if address:
            return address.district_image
        return None
    
    def get_address_by_location(self, selected_country, selected_city, selected_district):
        address = Address.query.filter_by(country=selected_country, city=selected_city, district=selected_district).first()
        return self._convert_to_dict(address) if address else None