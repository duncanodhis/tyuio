from flask import Blueprint, jsonify
from sqlalchemy import func, desc
from app import db
from services.metric_service import MetricService 
from flask import request, jsonify
from services.metric_service import MetricService


metric_routes = Blueprint("metric_routes", __name__)

@metric_routes.route("/api/top-buyers", methods=["GET"])
def get_top_buyers_controller():
    try:
        metric_service = MetricService()  # Create an instance of MetricService
        top_buyers_data = metric_service.get_top_buyers_data()
        return jsonify(top_buyers_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@metric_routes.route('/api/metrics', methods=['GET'])
def get_metrics():
    metrics_data_service = MetricService()
    metrics_data = metrics_data_service.calculate_metrics_data()  # Call your metrics service function here
    return jsonify(metrics_data)

@metric_routes.route("/api/summary", methods=["GET"])
def get_summary():
    summary_service = MetricService()
    summary_data = summary_service.get_summary_data()
    return jsonify(summary_data)

@metric_routes.route('/api/earnings', methods=['GET'])
def get_earnings():
    earnings_data =   MetricService()
    earnings_data_ = earnings_data.get_earnings()
    return jsonify(earnings_data_)

@metric_routes.route('/api/goods', methods=['GET'])
def get_goods():
    goods_service = MetricService()
    goods_data = goods_service.get_goods()
    return jsonify(goods_data)

@metric_routes.route('/api/sales', methods=['GET'])
def get_total_sales():
    sales_service = MetricService()
    total_sales_data = sales_service.get_total_sales()
    return jsonify(total_sales_data)

@metric_routes.route('/api/clients', methods=['GET'])
def get_clients():
    metric_service = MetricService()
    clients_data = metric_service.get_clients()
    return jsonify(clients_data)

@metric_routes.route('/api/sales_stat')
def get_sales_data():
    period = request.args.get('period', default='Day')  # Use 'request' instead of 'requests'
    metric_service = MetricService()
    sales_data = metric_service.get_sales_data(period)
    return jsonify({period: sales_data})

@metric_routes.route("/api/top-product-day", methods=["GET"])
def top_product_of_the_day():

    top_product_data_service =MetricService()
    top_product_data = top_product_data_service.get_top_product_of_the_day()

    if top_product_data:
        return jsonify(top_product_data)
    else:
        return jsonify({"message": "No top product found for the day"}), 404

@metric_routes.route("/api/latest-purchase", methods=["GET"])
def latest_purchase():

    latest_purchase_data=MetricService()
    latest_purchase_data = latest_purchase_data.get_latest_purchase()
    return jsonify(latest_purchase_data)


#Reviews
@metric_routes.route("/api/rating", methods=["GET"])
def get_customer_ratings_controller():
    try:
        average_rating_data =MetricService()
        average_rating = average_rating_data.get_customer_ratings()
        return jsonify( average_rating)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @metric_routes.route("/api/returnrate", methods=["GET"])
# def get_return_rate_controller():
#     try:
#         return_rate_data = MetricService()
#         return_rate = return_rate_data.get_return_rate()
#         return jsonify(return_rate)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

@metric_routes.route("/api/averageordervalue", methods=["GET"])
def get_average_order_value_controller():
    try:
        avg_order_value_data = MetricService()
        avg_order_value = avg_order_value_data.calculate_average_order_value()
        return jsonify(avg_order_value)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@metric_routes.route("/api/retention", methods=["GET"])
def get_retention_rate_controller():
    try:
        retention_rate_data = MetricService()
        retention_rate = retention_rate_data.get_retention_rate()
        return jsonify(retention_rate)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#doughnut chart
@metric_routes.route('/api/revenue-distribution-by-product', methods=['GET'])
def revenue_distribution_by_product():
    try:
        revenue_distribution_data = MetricService()
        revenue_distribution=  revenue_distribution_data.get_revenue_distribution_by_product()
        return jsonify(revenue_distribution), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@metric_routes.route('/api/customer-segmentation', methods=['GET'])
def get_customer_segmentation():
    try:
        # Calculate customer segmentation using the service
        segmentation_data_ = MetricService()
        segmentation_data = segmentation_data_.calculate_customer_segmentation()
        # Return the segmentation data as JSON
        return jsonify(segmentation_data), 200
    except Exception as e:
        # Handle any errors and return an error response
        return jsonify({'error': str(e)}), 500
    
@metric_routes.route('/api/sales-by-category', methods=['GET'])
def get_sales_by_category():
    try:
        sales_data_ = MetricService()
        sales_data = sales_data_.fetch_sales_by_category()
        return jsonify({'sales_by_category': sales_data}), 200
    except Exception as e:
        return jsonify({'error': 'Failed to fetch sales by category', 'details': str(e)}), 500