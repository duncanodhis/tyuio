from models.courier import Task
from app import db
from sqlalchemy import or_

class TaskService:
    def get_tasks(self):
        tasks = Task.query.all()
        return [self._convert_to_dict(task) for task in tasks]

    def get_task(self, task_id):
        task = Task.query.get(task_id)
        return self._convert_to_dict(task) if task else None

    def create_task(self, data):
        task = Task(**data)
        db.session.add(task)
        db.session.commit()
        return self._convert_to_dict(task)
    def update_task_treasures_and_status(self, task_id, current_treasures):
        task = Task.query.get(task_id)
        if task:
            task.number_of_treasures -= 1  # Reduce the number of treasures
            if task.number_of_treasures == 0:
                task.status = 'Completed'
            elif current_treasures < task.number_of_treasures:
                task.status = 'Incomplete'
            db.session.commit()
            return True
        return False

    def update_task(self, task_id, data):
        task = Task.query.get(task_id)
        if task:
            for key, value in data.items():
                setattr(task, key, value)
            db.session.commit()
            return self._convert_to_dict(task)
        return None

    def delete_task(self, task_id):
        task = Task.query.get(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
            return True
        return False

    def _convert_to_dict(self, task):
        if task:
            return {key: getattr(task, key) for key in task.__dict__.keys() if not key.startswith('_')}
        return None

    def get_tasks_for_courier(self, courier_id):
        tasks = Task.query.filter_by(courier_id=courier_id).all()
        return [self._convert_to_dict(task) for task in tasks]
    
    def get_pending_and_incomplete_tasks_for_courier(self, courier_id):
        tasks = Task.query.filter_by(courier_id=courier_id).filter(or_(Task.status == 'Pending', Task.status == 'Incomplete')).all()
        return [self._convert_to_dict(task) for task in tasks]