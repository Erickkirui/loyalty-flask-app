# will contain blueprint of the endpoints and path

from flask import Blueprint
from flask_restful import Api
from Server.Views.customerviews import GetAllCustomers,AddCustomer,CustomerResourcesById


Version_one = Blueprint('auth', __name__, url_prefix='/api/v1')
api = Api(Version_one)

# all path endpoints
api.add_resource(GetAllCustomers, '/customers')
api.add_resource(AddCustomer, '/customers')
api.add_resource(CustomerResourcesById, '/customers/<int:customer_id>')