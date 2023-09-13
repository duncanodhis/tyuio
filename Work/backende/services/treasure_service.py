from models.courier import Treasure  # Import the Treasure model
from models.courier import Task
from app import db

class TreasureService:
    def get_treasures(self):
        treasures = Treasure.query.all()
        return [self._convert_to_dict(treasure) for treasure in treasures]

    def get_treasure(self, treasure_id):
        treasure = Treasure.query.get(treasure_id)
        return self._convert_to_dict(treasure) if treasure else None

    def create_treasure(self,data):
        treasure = Treasure(**data)
        db.session.add(treasure)
        db.session.commit()
        return self._convert_to_dict(treasure)

    def retrieve_treasure(self, treasure_id):
        treasure = Treasure.query.get(treasure_id)
        if treasure:
            if treasure.status == 'pending':
                treasure.status = 'retrieved'
                treasure.taken = True
                db.session.commit()
                return self._convert_to_dict(treasure)
            else:
                return None, 'Treasure is not available for retrieval'
        else:
            return None, 'Treasure not found'

    def update_treasure(self, treasure_id, data):
        treasure = Treasure.query.get(treasure_id)
        if treasure:
            for key, value in data.items():
                setattr(treasure, key, value)
            db.session.commit()
            return self._convert_to_dict(treasure)
        return None

    def delete_treasure(self, treasure_id):
        treasure = Treasure.query.get(treasure_id)
        if treasure:
            db.session.delete(treasure)
            db.session.commit()
            return True
        return False

    def _convert_to_dict(self, treasure):
        if treasure:
            return {key: getattr(treasure, key) for key in treasure.__dict__.keys() if not key.startswith('_')}
        return None
