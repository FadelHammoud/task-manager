from enums import TaskPriority, TaskCategory
from datetime import datetime, timedelta

class TaskCreateValidator:
    @staticmethod
    def validate(data):
        if not data:
            return False, 'invalid JSON data'
        title = data.get('title')
        description = data.get('description')
        if not title or not description:
            return False, 'Missing required fields (title or description)'
        
        priority_str = data.get('priority')
        category_str = data.get('category')
        due_date_str = data.get('due_date')

        # validate priority enum
        try:
            priority = TaskPriority[priority_str.upper()] if priority_str else TaskPriority.LOW
            data['priority'] = priority
        except KeyError:
            return False, 'invalid priority'

        # validate category enum
        try:
            category = TaskCategory[category_str.upper()] if category_str else TaskCategory.OTHER
            data['category'] = category
        except KeyError:
            return False, 'invalid category'

        # parse due date if provided, else set default due date as tomorrow
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else datetime.now().date() + timedelta(days=1)
            data['due_date'] = due_date
        except ValueError:
            return False, 'invalid due date format. use YYYY-MM-DD.'
        return True, None

class TaskUpdateValidator:
    @staticmethod
    def validate(data):
        if not data:
            return False, 'invalid JSON data'
        title = data.get('title')
        description = data.get('description')
        completed = data.get('completed')
        priority_str = data.get('priority')
        category_str = data.get('category')
        due_date_str = data.get('due_date')

        # at least one field is provided to update
        if not title and not description and completed is None and priority_str is None and category_str is None and due_date_str is None:
            return False, 'No fields provided for update, provide at least one field to update'
        
        # validate priority enum if provided
        if priority_str:
          try:
            priority = TaskPriority[priority_str.upper()]
            data['priority'] = priority
          except KeyError:
            return False, 'invalid priority'

        # validate category enum if provided
        if priority_str:
          try:
            category = TaskCategory[category_str.upper()]
            data['category'] = category
          except KeyError:
              return False, 'invalid category'

        # validate due date if provided
        if due_date_str:
          try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
            data['due_date'] = due_date
          except ValueError:
              return False, 'invalid due date format. use YYYY-MM-DD.'
        
        return True, None
