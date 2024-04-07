from flask import request, jsonify, make_response
from functools import wraps

class OrderInterceptor:
    def __init__(self, app=None):
        self.app = app

    def intercept(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                order_param = request.args.get('order')

                if order_param:
                    order_parts = order_param.split(',')
                    order_by = order_parts[0]
                    order_dir = order_parts[1] if len(order_parts) > 1 else 'asc'
                else:
                    # default values
                    order_by = 'id'
                    order_dir = 'asc'

                # validate order_by && order dir
                if order_by not in ['id', 'title', 'description', 'completed', 'priority', 'category', 'due_date']:
                    return make_response(jsonify({'message': 'Invalid value for order by parameter'}), 400)

                if order_dir not in ['asc', 'desc']:
                    return make_response(jsonify({'message': 'Invalid value for order direction parameter'}), 400)

                request.order_by = order_by
                request.order_dir = order_dir

                return func(*args, **kwargs)
            except Exception as e:
                print("Exception:", e)
                return make_response(jsonify({'message': 'error intercepting request', 'error': str(e)}), 500)
        return wrapper
