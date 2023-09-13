from flask import Blueprint, jsonify
from services.statistics_service import StatisticsService

statistics_routes = Blueprint('statistics_routes', __name__)
statistics_service = StatisticsService()

@statistics_routes.route('/api/statistics', methods=['GET'])
def get_statistics():
    statistics = statistics_service.calculate_statistics()
    return jsonify(statistics)
