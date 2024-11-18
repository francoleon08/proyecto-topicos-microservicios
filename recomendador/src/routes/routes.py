from flask import Blueprint

bp = Blueprint('routes', __name__)

@bp.route('/', methods=['GET'])
def hello():
    return {'message': 'Hello, World!'}
