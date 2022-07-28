from flask import request
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from implemented import user_service
from service.decorators import admin_requered

user_ns = Namespace('users')


@user_ns.route('/')
class UsersView(Resource):
    @admin_requered
    def get(self):
        users = user_service.get_all()
        res_ussers = UserSchema(many=True).dump(users)
        return res_ussers, 200

    @admin_requered
    def post(self):
        req_json = request.json
        user = user_service.create(req_json)
        return "", 201, {"location": f"/users/{user.id}"}


@user_ns.route('/<int:uid>')
class UserView(Resource):
    @admin_requered
    def get(self, uid):
        user = user_service.get_one(uid)
        user_d = UserSchema().dump(user)
        return user_d, 200

    @admin_requered
    def put(self, uid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = uid
        user_service.update(req_json)
        return "", 204
