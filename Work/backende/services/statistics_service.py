from models.statistics import Statistic
from app  import db

class StatisticsService:
    def get_statistics(self):
        statistics = Statistic.query.all()
        return [self._convert_to_dict(stat) for stat in statistics]

    def get_statistic(self, stat_id):
        stat = Statistic.query.get(stat_id)
        return self._convert_to_dict(stat) if stat else None

    def create_statistic(self, data):
        stat = Statistic(**data)
        db.session.add(stat)
        db.session.commit()
        return self._convert_to_dict(stat)

    def update_statistic(self, stat_id, data):
        stat = Statistic.query.get(stat_id)
        if stat:
            for key, value in data.items():
                setattr(stat, key, value)
            db.session.commit()
            return self._convert_to_dict(stat)
        return None

    def delete_statistic(self, stat_id):
        stat = Statistic.query.get(stat_id)
        if stat:
            db.session.delete(stat)
            db.session.commit()
            return True
        return False

    def _convert_to_dict(self, stat):
        if stat:
            return {key: getattr(stat, key) for key in stat.__dict__.keys() if not key.startswith('_')}
        return None
