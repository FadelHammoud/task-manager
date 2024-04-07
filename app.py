from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from validators import TaskCreateValidator, TaskUpdateValidator
from os import environ
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from enums import TaskPriority, TaskCategory
from sqlalchemy_enums import SQLAlchemyEnum
from interceptor import OrderInterceptor
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
order_interceptor = OrderInterceptor()

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

# define the task table
class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(240), unique=False, nullable=False)
    completed = db.Column(db.Boolean(), default=False)
    priority = db.Column(SQLAlchemyEnum(TaskPriority), nullable=False, default=TaskPriority.LOW)
    category = db.Column(SQLAlchemyEnum(TaskCategory), nullable=False, default=TaskCategory.OTHER)
    due_date = db.Column(db.Date)

    def json(self):
        return {'id': self.id,
                'title': self.title,
                'description': self.description,
                'completed': self.completed,
                'priority': self.priority.value,
                'category': self.category.value,
                'due_date': self.due_date.strftime('%Y-%m-%d') if self.due_date else None
              }

with app.app_context():
  try:
      db.create_all()
  except Exception as e:
      print("Error creating database tables:", e)

# create a test route
@app.route('/test', methods=['GET'])
def test():
  return make_response(jsonify({'message': 'test route'}), 200)

# create a task
@app.route('/tasks', methods=['POST'])
def create_task():
  try:
    data = request.get_json()

    is_valid, error_message = TaskCreateValidator.validate(data)
    if not is_valid:
      return make_response(jsonify({'message': error_message}), 400)
    
    completed = data.get('completed', False)
    
    new_task = Task(title=data['title'], description=data['description'], completed=completed, priority=data['priority'], category=data['category'], due_date=data['due_date'])
    db.session.add(new_task)
    db.session.commit()
    return make_response(jsonify(new_task.json()), 201)
  except IntegrityError as e:
    db.session.rollback()
    return make_response(jsonify({'message': 'error creating task: Integrity Error, title already exists.', 'error': str(e)}), 400)
  except Exception as e:
    print("Exception:", e)
    return make_response(jsonify({'message': 'error creating task', 'error': str(e)}), 500)

# get all tasks
@app.route('/tasks', methods=['GET'])
@order_interceptor.intercept
def get_tasks():
  try:
    if request.order_dir == 'desc':
      tasks = Task.query.order_by(getattr(Task, request.order_by).desc()).all()
    else:
      tasks = Task.query.order_by(getattr(Task, request.order_by)).all()

    return make_response(jsonify([task.json() for task in tasks]), 200)
  except Exception as e:
    print("Exception:", e)
    return make_response(jsonify({'message': 'error getting tasks', 'error': str(e)}), 500)

# get a task by id
@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
  try:
    task = Task.query.filter_by(id=id).first()
    if task:
      return make_response(task.json(), 200)
    return make_response(jsonify({'message': 'task not found'}), 404)
  except Exception as e:
    print("Exception:", e)
    return make_response(jsonify({'message': 'error getting task', 'error': str(e)}), 500)

# update a task
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
  try:
    task = Task.query.filter_by(id=id).first()

    if not task:
      return make_response(jsonify({'message': 'task not found'}), 404)

    data = request.get_json()
    is_valid, error_message = TaskUpdateValidator.validate(data)
    if not is_valid:
      return make_response(jsonify({'message': error_message}), 400)
    
    if 'title' in data:
      task.title = data['title']
    if 'description' in data:
      task.description = data['description']
    if 'priority' in data:
      task.priority = data['priority']
    if 'category' in data:
      task.category = data['category']
    if 'due_date' in data:
      task.due_date = data['due_date']

    # update completed to true only
    if 'completed' in data and data['completed']:
      task.completed = data['completed']

    
    db.session.commit()
    return make_response(jsonify(task.json()), 200)
  except IntegrityError as e:
    db.session.rollback()
    return make_response(jsonify({'message': 'error updating task: Integrity Error, title already exists.', 'error': str(e)}), 400)
  except Exception as e:
    print("Exception:", e)
    return make_response(jsonify({'message': 'error updating task', 'error': str(e)}), 500)

# delete a task
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
  try:
    task = Task.query.filter_by(id=id).first()
    if task:
      db.session.delete(task)
      db.session.commit()
      return make_response(jsonify({'message': 'task deleted'}), 200)
    return make_response(jsonify({'message': 'task not found'}), 404)
  except Exception as e:
    print("Exception:", e)
    return make_response(jsonify({'message': 'error deleting task', 'error': str(e)}), 500)

################################################
###################### BONUS ###################
################################################

# get tasks by priority
@app.route('/tasks/priority/<string:priority>', methods=['GET'])
@order_interceptor.intercept
def get_tasks_by_priority(priority):
    try:
        priority_enum = TaskPriority[priority.upper()]
    except KeyError:
        return make_response(jsonify({'message': 'Invalid priority'}), 400)
    
    if request.order_dir == 'desc':
      tasks = Task.query.filter_by(priority=priority_enum).order_by(getattr(Task, request.order_by).desc()).all()
    else:
      tasks = Task.query.filter_by(priority=priority_enum).order_by(getattr(Task, request.order_by)).all()

    return make_response(jsonify([task.json() for task in tasks]), 200)

# get tasks by category
@app.route('/tasks/category/<string:category>', methods=['GET'])
@order_interceptor.intercept
def get_tasks_by_category(category):
    try:
        category_enum = TaskCategory[category.upper()]
    except KeyError:
        return make_response(jsonify({'message': 'Invalid category'}), 400)
    
    if request.order_dir == 'desc':
      tasks = Task.query.filter_by(category=category_enum).order_by(getattr(Task, request.order_by).desc()).all()
    else:
      tasks = Task.query.filter_by(category=category_enum).order_by(getattr(Task, request.order_by)).all()

    return make_response(jsonify([task.json() for task in tasks]), 200)

# get tasks by due date
@app.route('/tasks/due/<date>', methods=['GET'])
@order_interceptor.intercept
def get_tasks_due_on(date):
    try:
        due_date = datetime.strptime(date, '%Y-%m-%d').date()

        if request.order_dir == 'desc':
          tasks = Task.query.filter_by(due_date=due_date).order_by(getattr(Task, request.order_by).desc()).all()
        else:
          tasks = Task.query.filter_by(due_date=due_date).order_by(getattr(Task, request.order_by)).all()

        return make_response(jsonify([task.json() for task in tasks]), 200)
    except ValueError:
        return make_response(jsonify({'message': 'Invalid date format. Use YYYY-MM-DD.'}), 400)


if __name__ == '__main__':
    app.run(debug=True, port=4000)