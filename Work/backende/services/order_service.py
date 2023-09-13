from models.order import Order
from datetime import datetime, timedelta
from models.courier import Treasure
from models.product import Product
from app import db

class OrderService:
    def get_orders(self):
        orders = Order.query.all()
        order_data = []
        
        for order in orders:
            order_dict = self._convert_to_dict(order)
            
            # Include product name
            if order.product_id:
                product = Product.query.get(order.product_id)
                order_dict['product_name'] = product.name
            
            # Check payment status
            if order.transaction_id:
                order_dict['payment_status'] = 'Paid'
            else:
                order_dict['payment_status'] = 'Not Paid'
            
            # Include treasure image
            if order.treasure_id:
                treasure = Treasure.query.get(order.treasure_id)
                order_dict['treasure_image'] = treasure.image_url
            
            order_data.append(order_dict)
        
        
        return order_data

    def get_order(self, order_id):
        order = Order.query.get(order_id)
        return self._convert_to_dict(order) if order else None

    def create_order(self, data):
        order = Order(**data)
        db.session.add(order)
        db.session.commit()
        return order.id

    def update_order(self, order_id, data):
        order = Order.query.get(order_id)
        if order:
            for key, value in data.items():
                setattr(order, key, value)
            db.session.commit()
            return self._convert_to_dict(order)
        return None

    def delete_order(self, order_id):
        order = Order.query.get(order_id)
        if order:
            db.session.delete(order)
            db.session.commit()
            return True
        return False
    
    def fulfill_order(self, order, treasure):
        if order.treasure_id is None and treasure.status == 'available':
            order.treasure_id = treasure.id
            treasure.status = 'given'
            db.session.commit()
            return True
        return False

    def release_treasure(self, order):
        if order.treasure_id is not None:
            treasure = Treasure.query.get(order.treasure_id)
            if treasure and treasure.status == 'given':
                current_time = datetime.utcnow()
                release_time = treasure.given_at + timedelta(days=2)  # Adjust the release period as needed
                if current_time >= release_time:
                    treasure.status = 'available'
                    order.treasure_id = None
                    db.session.commit()
                    return True
        return False

    def associate_order_with_treasure(self, order_id):
        order = Order.query.get(order_id)
        if order:
            unassigned_orders = [order]

            available_treasures = Treasure.query.filter(Treasure.taken == False).all()

            for order in unassigned_orders:
                suitable_treasures = [
                    treasure for treasure in available_treasures
                    if treasure.task.product_id == order.product_id and treasure.task.product.address.district == order.product.address.district
                ]

                if not suitable_treasures:
                    suitable_treasures = [
                        treasure for treasure in available_treasures
                        if treasure.task.product_id == order.product_id and treasure.task.product.address.city == order.product.address.city
                    ]

                if suitable_treasures:
                    selected_treasure = suitable_treasures[0]
                    selected_treasure.taken = True                
                    selected_treasure.status = 'retrieved'
                    order.treasure_id = selected_treasure.id
                    db.session.commit()

                    return {
                        'message': f"Order {order.id} associated with Treasure {selected_treasure.id}",
                        'associated_treasure': {
                            'id': selected_treasure.id,
                            'description': selected_treasure.description,
                            'coordinates': selected_treasure.coordinates,
                            'image_url': selected_treasure.image_url,
                            'status': selected_treasure.status,
                            'taken': selected_treasure.taken
                        }
                    }
                else:
                    return f"No available treasures for Order {order.id}"

        return "Order not found"
   
    def get_orders_by_telegram_id(self, telegram_id):
        # Retrieve orders for the customer with the given Telegram ID
        orders = Order.query.filter_by(telegram_id=telegram_id).all()
        
        order_data = []
        
        for order in orders:
            order_dict = self._convert_to_dict(order)
            
            # Include product name
            if order.product_id:
                product = Product.query.get(order.product_id)
                order_dict['product_name'] = product.name
            
            # Check payment status
            if order.transaction_id:
                order_dict['payment_status'] = 'Paid'
            else:
                order_dict['payment_status'] = 'Not Paid'
            
            # Include treasure image
            if order.treasure_id:
                treasure = Treasure.query.get(order.treasure_id)
                order_dict['treasure_image'] = treasure.image_url
            
            order_data.append(order_dict)
        
        return order_data
    def _convert_to_dict(self, order):
        if order:
            return {key: getattr(order, key) for key in order.__dict__.keys() if not key.startswith('_')}
        return None

    # def get_orders_with_images(self):
    #     orders = Order.query.all()
       
    #     orders_with_images = []
    #     for order in orders:

    #         truncated_transaction_id = order.transaction_id[:5] if order.transaction_id else None
            
    #         payment_status = "Paid" if order.transaction_id else "Not Paid"

    #         orders_with_images.append({
    #             'id': order.id,
    #             'quantity': order.quantity,
    #             'number_of_orders': order.number_of_orders,
    #             'quantity_unit': order.quantity_unit,
    #             'total_price': order.total_price,
    #             'product_name': order.product,
    #             'customer_telegram_id': order.customer.telegram_id,
    #             'payment_status': payment_status,
    #             'treasure_id': order.treasure_id,
    #             'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    #             # Add more attributes as needed
    #         })

    #     return orders_with_images
