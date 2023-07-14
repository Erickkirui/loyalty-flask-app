from flask_restful import Resource
from app import db
from Server.Models.LoyaltyPoints import LoyaltyPoints
from flask import request


class GetAllLoyaltyPoints(Resource):
    def get(self):
        loyalty_points = LoyaltyPoints.query.all()
        loyalty_points_list = [{
            "id": loyalty_point.id,
            "customer_id": loyalty_point.customer_id,
            "points": loyalty_point.points
        } for loyalty_point in loyalty_points]

        return {'loyalty_points': loyalty_points_list}, 200


class LoyaltyPointsResource(Resource):
    def get(self, loyalty_points_id):
        loyalty_points = LoyaltyPoints.query.get(loyalty_points_id)
        if loyalty_points:
            return {
                "id": loyalty_points.id,
                "customer_id": loyalty_points.customer_id,
                "points": loyalty_points.points
            }, 200
        else:
            return {"error": "LoyaltyPoints not found"}, 404

    def patch(self, loyalty_points_id):
        loyalty_points = LoyaltyPoints.query.get(loyalty_points_id)
        if not loyalty_points:
            return {"error": "LoyaltyPoints not found"}, 404

        data = request.get_json()
        points = data.get('points')

        if not points:
            return {'error': 'Invalid data. Please provide points.'}, 400

        loyalty_points.points = points
        db.session.commit()

        return {'message': 'LoyaltyPoints updated successfully'}, 200
