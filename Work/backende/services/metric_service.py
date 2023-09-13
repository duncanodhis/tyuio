from sqlalchemy import func
from models.courier import Task, Treasure
from app import db
from sqlalchemy import func
from datetime import datetime, timedelta
from models.courier import Treasure
from models.customer import Customer
from models.order import Order
from models.customer import Customer
from models.product import Product
from models.address import Address
from models.review import Review
from sqlalchemy import func
from datetime import date, timedelta
from models.product import Category

class MetricService:

    def get_summary_data(self):
        total_value = 0
        remaining_quantity = 0
        sold_today = 0

        orders = Order.query.all()
        treasures = Treasure.query.filter_by(taken=False).all()

        for order in orders:
            total_value += order.total_price
            sold_today += order.number_of_orders

        for treasure in treasures:
            remaining_quantity += treasure.number_of_treasures

        return {
            "total_value": total_value,
            "remaining_quantity": remaining_quantity,
            "sold_today": sold_today,
        }

    def get_earnings(self):
        earnings = db.session.query(
            func.strftime('%Y-%m-%d', Order.created_at).label('period'),
            func.sum(Order.total_price).label('earnings')
        ).group_by(func.strftime('%Y-%m-%d', Order.created_at)).all()

        earnings_data = [
            {
                "period": earnings_record.period,
                "earnings": earnings_record.earnings
            }
            for earnings_record in earnings
        ]

        return earnings_data
   
    def get_total_sales(self):
        sales = db.session.query(
            func.strftime('%Y-%m-%d', Order.created_at).label('period'),
            func.count(Order.id).label('sales')
        ).group_by(func.strftime('%Y-%m-%d', Order.created_at)).all()

        sales_data = [
            {
                "period": sales_record.period,
                "sales": sales_record.sales
            }
            for sales_record in sales
        ]

        return sales_data
    
    def get_clients(self):
        clients = db.session.query(
            func.strftime('%Y-%m', Customer.created_at).label('period'),
            func.count(Customer.id).label('clients')
        ).group_by(func.strftime('%Y-%m', Customer.created_at)).all()

        clients_data = [
            {
                "period": client_record.period,
                "clients": client_record.clients
            }
            for client_record in clients
        ]

        return clients_data

    def get_goods(self):
        goods = db.session.query(
            Product.id,
            Product.name,
            Product.package_currency,
            Product.package_description,
            Product.package_price,
            Product.selling_currency,
            Product.selling_description,
            Product.selling_price
        ).all()

        goods_data = [
            {
                "id": good.id,
                "name": good.name,
                "package_currency": good.package_currency,
                "package_description": good.package_description,
                "package_price": good.package_price,
                "selling_currency": good.selling_currency,
                "selling_description": good.selling_description,
                "selling_price": good.selling_price
            }
            for good in goods
        ]

        return goods_data

    def get_metrics(self):
        total_orders = Order.query.count()
        total_revenue = Order.query.with_entities(func.sum(Order.total_price)).scalar()
        average_order_value = total_revenue / total_orders if total_orders else 0

        metrics_data = {
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "average_order_value": average_order_value,
        }
        return metrics_data

    def get_weekly_clients(self):
        current_date = datetime.utcnow()
        week_start = current_date - timedelta(days=current_date.weekday())
        week_end = week_start + timedelta(days=6)

        new_clients_count = Customer.query.filter(Customer.created_at >= week_start, Customer.created_at <= week_end).count()

        weekly_clients_data = {
            "week_start": week_start.date().isoformat(),
            "week_end": week_end.date().isoformat(),
            "new_clients_count": new_clients_count,
        }
        return weekly_clients_data
 
    def calculate_metrics_data(self):
        # Calculate metrics and retrieve necessary data here
        total_sales = self.calculate_total_sales()
        total_earnings = self.calculate_total_earnings()
        profit_margin = self.calculate_profit_margin()
        avg_order_value = self.calculate_average_order_value()
        customer_lifetime_value = self.calculate_customer_lifetime_value()

        # Construct metrics data dictionary
        metrics_data = {
            'sales': total_sales,
            'earnings': total_earnings,
            'profitMargin': profit_margin,
            'avgOrderValue': avg_order_value,
            'customerLifetime': customer_lifetime_value,
        }
        return metrics_data
    
    def calculate_total_sales(self):
        # Query your database to get the total number of sales
        # You might use the Order table and count the number of records
        total_sales = db.session.query(func.count(Order.id)).scalar()
        return total_sales

    def calculate_total_earnings(self):
        # Query your database to get the total earnings
        # You might sum up the total_price from the Order table
        total_earnings = db.session.query(func.sum(Order.total_price)).scalar()
        return total_earnings

    def calculate_profit_margin(self):
        # Calculate the profit margin using your business logic
        # You might calculate it based on total earnings and costs
        profit_margin = (calculate_total_earnings() - calculate_total_costs()) / calculate_total_earnings()
        return profit_margin

    def calculate_average_order_value(self):
        # Calculate the average order value using your business logic
        # You might calculate it based on total earnings and the number of orders
        average_order_value = calculate_total_earnings() / calculate_total_sales()
        return average_order_value

    def calculate_customer_lifetime_value(self):
        # Calculate the customer lifetime value using your business logic
        # You might consider the average order value, retention rate, and customer lifetime
        customer_lifetime_value = calculate_average_order_value() * calculate_customer_lifetime()
        return customer_lifetime_value

    def calculate_metrics_data(self):
        # Calculate metrics and retrieve necessary data here
        total_sales = self.calculate_total_sales()
        total_earnings = self.calculate_total_earnings()
        profit_margin = self.calculate_profit_margin()
        avg_order_value = self.calculate_average_order_value()
        customer_lifetime_value = self.calculate_customer_lifetime_value()

        # Construct metrics data dictionary
        metrics_data = {
            'sales': total_sales,
            'earnings': total_earnings,
            'profitMargin': profit_margin,
            'avgOrderValue': avg_order_value,
            'customerLifetime': customer_lifetime_value,
        }
        return metrics_data
    
    def calculate_total_sales(self):
        # Query your database to get the total number of sales
        # You might use the Order table and count the number of records
        total_sales = db.session.query(func.count(Order.id)).scalar()
        return total_sales

    def calculate_total_earnings(self):
        # Query your database to get the total earnings
        # You might sum up the total_price from the Order table
        total_earnings = db.session.query(func.sum(Order.total_price)).scalar()
        return total_earnings
    def calculate_total_costs(self):
        # Query your database to get the total cost of commissions for tasks with taken treasures
        total_costs = db.session.query(func.sum(Task.commission).label('total_costs')) \
            .join(Treasure, Task.id == Treasure.task_id) \
            .filter(Treasure.taken == True) \
            .scalar()

        if total_costs is None:
            return 0.0  # Return zero if the result is None
        return total_costs

    def calculate_profit_margin(self):
        total_earnings = self.calculate_total_earnings()
        total_costs = self.calculate_total_costs()
        print("total earning",total_earnings)
        print("total cost",total_costs)
        
      
        if total_earnings == 0:
            profit_margin = 0
        else:
            profit_margin = (total_earnings - total_costs) / total_earnings
            # profit_margin = (self.calculate_total_earnings() - self.calculate_total_costs()) / self.calculate_total_earnings()


        return profit_margin
    
    # def calculate_average_order_value(self):
    #     # Calculate the average order value using your business logic
    #     # You might calculate it based on total earnings and the number of orders
    #     average_order_value = self.calculate_total_earnings() / self.calculate_total_sales()
    #     return average_order_value
   
    from datetime import datetime, timedelta

    def calculate_average_order_value(self, time_period='month'):
        # Calculate the start and end dates of the time period
        end_date = datetime.utcnow()
        if time_period == 'month':
            start_date = end_date - timedelta(days=30)  # You can adjust the number of days as needed for the month
        elif time_period == 'year':
            start_date = end_date - timedelta(days=365)  # You can adjust the number of days as needed for the year
        else:
            # Handle other time periods or invalid inputs here
            return None
        
        # Query your database to get the total earnings for the specified time period
        total_earnings = db.session.query(func.sum(Order.total_price)).filter(Order.created_at >= start_date, Order.created_at <= end_date).scalar()
        
        # Query your database to get the total number of sales for the specified time period
        total_sales = db.session.query(func.count(Order.id)).filter(Order.created_at >= start_date, Order.created_at <= end_date).scalar()

        if total_sales == 0:
            average_order_value = 0  # Handle the case where there are no sales
        else:
            average_order_value = total_earnings / total_sales

        # Format the result similar to 'sales' data
        formatted_average_order_value = [
            {
                'period': start_date.strftime('%Y-%m-%d'),
                'average_order_value': average_order_value,
            }
        ]

        return formatted_average_order_value
    
    def calculate_customer_lifetime_value(self):
        # Calculate the customer lifetime value using your business logic
        # You might consider the average order value, retention rate, and customer lifetime
        customer_lifetime_value = self.calculate_average_order_value() * self.calculate_customer_lifetime()
        return customer_lifetime_value
    
    def calculate_customer_lifetime(self):
        # Implement your customer lifetime calculation logic here
        # For example, you might consider the average number of orders per customer
        # and the average time span a customer remains active

        average_orders_per_customer = self.calculate_average_orders_per_customer()
        average_customer_lifespan = self.calculate_average_customer_lifespan()

        customer_lifetime = average_orders_per_customer * average_customer_lifespan
        return customer_lifetime

    def calculate_average_orders_per_customer(self):
        total_orders = Order.query.count()
        total_customers = Customer.query.count()

        if total_customers == 0:
            return 0

        average_orders_per_customer = total_orders / total_customers
        return average_orders_per_customer

    def calculate_average_customer_lifespan(self):

        # Calculate the average lifespan of customers based on their first and last order dates

        # Get the earliest order date
        earliest_order_date = db.session.query(func.min(Order.created_at)).scalar()

        # Get the latest order date
        latest_order_date = db.session.query(func.max(Order.created_at)).scalar()

        if earliest_order_date is None or latest_order_date is None:
            return 0

        # Calculate the time span between the earliest and latest order dates
        time_span = latest_order_date - earliest_order_date

        # Calculate the average customer lifespan in days
        average_customer_lifespan = time_span.days / Customer.query.count()
        return average_customer_lifespan

    def get_sales_data(self, period):
        sales_data = []

        if period == 'Day':
            sales_data = self.get_daily_sales()
        elif period == 'Week':
            sales_data = self.get_weekly_sales()
        elif period == 'Month':
            sales_data = self.get_monthly_sales()
        elif period == '90 Days':
            sales_data = self.get_90_days_sales()
        elif period == 'Year':
            sales_data = self.get_annual_sales()
        elif period == 'Half Year':
            sales_data = self.get_semi_annual_sales()
        
        return sales_data

    def get_daily_sales(self):
        # Query your database to get daily sales data
        # You might use the Order table and group by day
        daily_sales = db.session.query(
            func.strftime('%Y-%m-%d', Order.created_at).label('period'),
            func.count(Order.id).label('sales')
        ).group_by(func.strftime('%Y-%m-%d', Order.created_at)).all()

        daily_sales_data = [
            {
                "period": sale_record.period,
                "sales": sale_record.sales
            }
            for sale_record in daily_sales
        ]

        return daily_sales_data
  
    def get_monthly_sales(self):
        monthly_sales = db.session.query(
            func.strftime('%Y-%m', Order.created_at).label('period'),
            func.count(Order.id).label('sales')
        ).group_by(func.strftime('%Y-%m', Order.created_at)).all()

        monthly_sales_data = [
            {
                "period": sale_record.period,
                "sales": sale_record.sales
            }
            for sale_record in monthly_sales
        ]

        return monthly_sales_data
    
    def get_weekly_sales(self):
        weekly_sales = db.session.query(
            func.strftime('%Y-%W', Order.created_at).label('period'),
            func.count(Order.id).label('sales')
        ).group_by(func.strftime('%Y-%W', Order.created_at)).all()

        weekly_sales_data = [
            {
                "period": sale_record.period,
                "sales": sale_record.sales
            }
            for sale_record in weekly_sales
        ]

        return weekly_sales_data

    def get_90_days_sales(self):
        # Calculate the date 90 days ago from the current date
        ninety_days_ago = datetime.utcnow() - timedelta(days=90)

        # Query sales data for the last 90 days
        ninety_days_sales = db.session.query(
            func.strftime('%Y-%m-%d', Order.created_at).label('period'),
            func.count(Order.id).label('sales')
        ).filter(Order.created_at >= ninety_days_ago).group_by(func.strftime('%Y-%m-%d', Order.created_at)).all()

        ninety_days_sales_data = [
            {
                "period": sale_record.period,
                "sales": sale_record.sales
            }
            for sale_record in ninety_days_sales
        ]

        return ninety_days_sales_data

    def get_annual_sales(self):
        # Query sales data for each year
        annual_sales = db.session.query(
            func.strftime('%Y', Order.created_at).label('period'),
            func.count(Order.id).label('sales')
        ).group_by(func.strftime('%Y', Order.created_at)).all()

        annual_sales_data = [
            {
                "period": sale_record.period,
                "sales": sale_record.sales
            }
            for sale_record in annual_sales
        ]

        return annual_sales_data

    def get_semi_annual_sales(self):
        # Calculate the date 6 months ago from the current date
        six_months_ago = datetime.utcnow() - timedelta(days=180)

        # Query sales data for the last 6 months
        semi_annual_sales = db.session.query(
            func.strftime('%Y-%m', Order.created_at).label('period'),
            func.count(Order.id).label('sales')
        ).filter(Order.created_at >= six_months_ago).group_by(func.strftime('%Y-%m', Order.created_at)).all()

        semi_annual_sales_data = [
            {
                "period": sale_record.period,
                "sales": sale_record.sales
            }
            for sale_record in semi_annual_sales
        ]

        return semi_annual_sales_data


    def get_top_buyers_data(self):
        top_buyers_data = []

        top_buyers = db.session.query(Customer.username,
                                    func.sum(Order.total_price).label('total_purchase')) \
            .join(Order, Customer.telegram_id == Order.telegram_id) \
            .group_by(Customer.username) \
            .order_by(func.sum(Order.total_price).desc()) \
            .limit(10)
        
        for username, total_purchase in top_buyers:
            most_bought_product = db.session.query(Product.name, func.count(Product.id).label('count')) \
                .join(Order, Product.id == Order.product_id) \
                .filter(Order.telegram_id == Customer.telegram_id) \
                .group_by(Product.name) \
                .order_by(func.count(Product.id).desc()) \
                .first()
            
            top_buyers_data.append({
                'username': username,
                'totalPurchase': total_purchase,
                'mostBoughtProduct': most_bought_product[0] if most_bought_product else None,
            })

        return top_buyers_data

    def get_top_product_of_the_day(self):
        current_date = date.today()

        top_product = db.session.query(
            Product.name,
            func.sum(Order.quantity).label("sales")
        ).join(Order, Order.product_id == Product.id)\
            .filter(Order.created_at >= current_date, Order.created_at < current_date + timedelta(days=1))\
            .group_by(Product.id, Product.name)\
            .order_by(func.sum(Order.quantity).desc())\
            .first()

        if top_product:
            top_product_data = {
                "product": top_product.name,
                "sales": top_product.sales
            }
            return top_product_data
        else:
            return {
                "product": "No sales",
                "sales": 0
            }

    def get_latest_purchase(self):
        product_id, telegram_id = self.get_latest_order()

        if product_id and telegram_id:
            product_details = self.get_product_details(product_id)
            buyer_details = self.get_buyer_details(telegram_id)

            if product_details and buyer_details:
                latest_purchase_data = {
                    "product": product_details,
                    "buyer": buyer_details
                }
                return latest_purchase_data

        return {
            "product": "No purchases",
            "buyer": "N/A"
        }

    def get_latest_order(self):
        latest_order = db.session.query(
            Order.product_id,
            Order.telegram_id
        ).order_by(Order.created_at.desc()).first()

        if latest_order:
            return latest_order.product_id, latest_order.telegram_id
        return None, None
    
    def get_product_details(self,product_id):
        product = Product.query.get(product_id)
        
        if product:
            product_details = {
                "name": product.name,
                "package_price": product.selling_price,
                "package_currency": product.selling_currency,
                "package_weight": product.selling_weight,
                "package_weight_measurement": product.selling_weight_measurement
            }
            return product_details
        return None
    
    def get_buyer_details(self,telegram_id):
        buyer = Customer.query.filter_by(telegram_id=telegram_id).first()
        
        if buyer:
            buyer_details = {
                "username": buyer.username,
                "balance": buyer.balance
            }
            return buyer_details
        return None


#reviews
    def get_customer_ratings(self, time_period='month'):
        # Calculate the return rate using your business logic and a specified time period
        
        # Calculate the start and end dates of the time period
        end_date = datetime.utcnow()
        if time_period == 'month':
            start_date = end_date - timedelta(days=30)  # You can adjust the number of days as needed for the month
        elif time_period == 'year':
            start_date = end_date - timedelta(days=365)  # You can adjust the number of days as needed for the year
        else:
            # Handle other time periods or invalid inputs here
            return None
        
        # Query your database to get the total number of orders for the specified time period
        total_orders = db.session.query(func.count(Order.id)).filter(Order.created_at >= start_date, Order.created_at <= end_date).scalar()
        
        # Query your database to get the number of orders with reviews for the specified time period
        orders_with_reviews = db.session.query(Order).join(Review, Order.id == Review.order_id).filter(
            Order.created_at >= start_date, Order.created_at <= end_date
        ).count()

        # Calculate the return rate
        return_rate = 0.0 if total_orders == 0 else (total_orders - orders_with_reviews) / total_orders

        # Format the result similar to 'sales' data
        formatted_return_rate = [
            {
                'period': start_date.strftime('%Y-%m-%d'),
                'return_rate': round(return_rate, 2),  # Round the return rate to 2 decimal places
            }
        ]

        return formatted_return_rate

    def get_average_order_value(self):
        # Calculate the average order value using your business logic
        # Assuming you have data for each month

        # Example: Calculate average order value for each month
        monthly_data = []
        for month in range(1, 13):  # Assuming data for 12 months
            total_revenue = db.session.query(
                func.sum(Order.total_price)
            ).filter(
                db.extract('month', Order.created_at) == month
            ).scalar()
            total_orders = Order.query.filter(
                db.extract('month', Order.created_at) == month
            ).count()

            avg_order_value = 0.0 if total_orders == 0 else total_revenue / total_orders
            monthly_data.append(round(avg_order_value, 2))  # Round the avg order value to 2 decimal places

        return {
            "averageOrderValue": monthly_data
        }

    def get_retention_rate(self, time_period='month'):
        # Calculate the customer retention rate using your business logic and a specified time period
        
        # Calculate the start and end dates of the time period
        end_date = datetime.utcnow()
        if time_period == 'month':
            start_date = end_date - timedelta(days=30)  # You can adjust the number of days as needed for the month
        elif time_period == 'year':
            start_date = end_date - timedelta(days=365)  # You can adjust the number of days as needed for the year
        else:
            # Handle other time periods or invalid inputs here
            return None
        
        # Query your database to get the total number of customers
        total_customers = db.session.query(func.count(Customer.id)).scalar()
        
        # Query your database to get the number of returning customers for the specified time period
        returning_customers = db.session.query(Customer).join(
            Order, Customer.telegram_id == Order.telegram_id
        ).filter(
            Order.created_at >= start_date, Order.created_at <= end_date
        ).group_by(Customer.telegram_id).having(func.count() > 1).count()

        # Calculate the retention rate
        retention_rate = 0.0 if total_customers == 0 else returning_customers / total_customers

        # Format the result similar to 'sales' data
        formatted_retention_rate = [
            {
                'period': start_date.strftime('%Y-%m-%d'),
                'retention_rate': round(retention_rate, 2),  # Round the retention rate to 2 decimal places
            }
        ]

        return formatted_retention_rate

    def get_revenue_distribution_by_product(self):
        # Use SQLAlchemy to query the database and calculate revenue distribution by product
        # Assuming you have a 'Product' model with a 'name' attribute
        revenue_distribution = db.session.query(
            db.func.sum(Order.total_price).label('revenue'),
            Product.name.label('product_name')
        ).join(Product, Order.product_id == Product.id).group_by(Product.name).all()

        # Convert the result to a list of dictionaries
        revenue_distribution_data = [
            {
                'product_name': row.product_name,
                'revenue': row.revenue
            }
            for row in revenue_distribution
        ]

        return revenue_distribution_data
    
    def calculate_customer_segmentation(self):
        # Define your segmentation criteria and logic here
        # For example, grouping by product and counting the number of orders
        segmentation_query = db.session.query(
            Product.name,
            func.count(Order.id).label('order_count')
        ).join(Order, Order.product_id == Product.id).group_by(Product.name)

        # Fetch the results
        segmentation_data = segmentation_query.all()

        # Convert the result to a list of dictionaries
        customer_segmentation = [
            {
                'product_name': row.name,
                'order_count': row.order_count,
            }
            for row in segmentation_data
        ]

        return customer_segmentation
    
    def fetch_sales_by_category(self):
        # Define the query to fetch sales by category
        sales_query = db.session.query(
            Category.name,
            func.sum(Order.total_price).label('total_sales')
        ).join(Product, Product.category_id == Category.id).join(Order, Order.product_id == Product.id).group_by(Category.name)

        # Fetch the results
        sales_data = sales_query.all()

        # Convert the result to a list of dictionaries
        sales_by_category = [
            {
                'category_name': row.name,
                'total_sales': row.total_sales,
            }
            for row in sales_data
        ]

        return sales_by_category
    



