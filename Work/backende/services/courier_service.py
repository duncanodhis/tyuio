from models.courier import Courier
from app import db
# from sqlalchemy.orm import joinedload

class CourierService:
    def get_couriers(self):
        couriers = Courier.query.all()
        return [self._convert_to_dict(courier) for courier in couriers]

    def get_courier(self, courier_id):
        courier = Courier.query.get(courier_id)
        return self._convert_to_dict(courier) if courier else None

    def create_courier(self, data):
        courier = Courier(**data)
        db.session.add(courier)
        db.session.commit()
        return self._convert_to_dict(courier)

    def update_courier(self, courier_id, data):
        courier = Courier.query.get(courier_id)
        if courier:
            for key, value in data.items():
                setattr(courier, key, value)
            db.session.commit()
            return self._convert_to_dict(courier)
        return None
    
    def update_courier_total_earning(self, courier_id):
        courier = Courier.query.options(db.joinedload(Courier.tasks)).get(courier_id)
        if courier:
            total_earning = 0.0

            for task in courier.tasks:
                if task.status == "complete" or task.status == "incomplete":
                    task_earning = sum([treasure.commission for treasure in task.treasures if treasure.taken])
                    total_earning += task_earning

            courier.total_earning = total_earning
            courier.commission_currency = "USD"  # Set a default value
            db.session.commit()

            return courier.total_earning

    def delete_courier(self, courier_id):
        courier = Courier.query.get(courier_id)
        if courier:
            db.session.delete(courier)
            db.session.commit()
            return True
        return False

    def _convert_to_dict(self, courier):
        if courier:
            return {key: getattr(courier, key) for key in courier.__dict__.keys() if not key.startswith('_')}
        return None
 
    def get_couriers_with_tasks(self):
        couriers_with_tasks = Courier.query.options(db.joinedload(Courier.tasks)).all()
        return [self._convert_to_dict_task(courier) for courier in couriers_with_tasks]

    def _convert_to_dict_task(self, courier):
        if courier:
            courier_data = self._convert_to_dict(courier)
            courier_data['tasks'] = [self._convert_task_to_dict(task) for task in courier.tasks]
            return courier_data
        return None
    def authenticate_courier(self, username, password):
        courier = Courier.query.filter_by(name=username).first()

        if courier and courier.password == password:
            return self._convert_to_dict(courier)
        
        return None
    
    def get_courier_earning(self, courier_id):
        courier = self.get_courier(courier_id)
        if courier:
            total_earning = sum([task.commission for task in courier.tasks if task.status == "complete"])
            return total_earning
        return 0
    
    def _convert_task_to_dict(self, task):
        if task:
            task_data = {
                'id': task.id,
                'name': task.name,
                'area_of_distribution': task.area_of_distribution,
                'commission': task.commission,
                'commission_currency': task.commission_currency,
                'cost_of_item': task.cost_of_item,
                'weight_of_item': task.weight_of_item,
                'item_weight_measurement': task.item_weight_measurement,
                'address': task.address,
                'number_of_items': task.number_of_items,
                'number_of_treasures': task.number_of_treasures,
                'status': task.status,
                'created_at': task.created_at,
                'updated_at': task.updated_at,
                'courier_id': task.courier_id,
                'product_id': task.product_id,
                'treasures': [treasure.id for treasure in task.treasures]
            }
            return task_data
        return None
