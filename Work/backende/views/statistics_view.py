from flask import Blueprint, jsonify
from services.statistics_service import StatisticsService

statistics_view = Blueprint('statistics_view', __name__)
statistics_service = StatisticsService()

@statistics_view.route('/statistics', methods=['GET'])
def get_statistics():
    statistics = statistics_service.calculate_statistics()
    return jsonify(statistics)
