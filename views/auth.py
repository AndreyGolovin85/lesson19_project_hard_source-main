"""
`POST /auth` — получает логин и пароль из Body запроса в виде JSON, далее проверяет соотвествие с данными в БД
(есть ли такой пользователь, такой ли у него пароль)
и если всё оk — генерит пару access_token и refresh_token и отдает их в виде JSON.

`PUT /auth` — получает refresh_token из Body запроса в виде JSON, далее проверяет refresh_token и если он не истек и
валиден — генерит пару access_token и refresh_token и отдает их в виде JSON.
"""
from flask import request
from flask_restx import Namespace, Resource

from implemented import auth_service

auth_ns = Namespace("auth")


@auth_ns.route("/")
class AuthView(Resource):
    def post(self):
        req_json = request.json
        username = req_json.get("username")
        password = req_json.get("password")
        if not (username or password):
            return "Введите логин или пароль", 400

        tokens = auth_service.generate_tokens(username, password)
        if tokens:
            return tokens
        return "Ошибка в запросе", 400

    def put(self):
        req_json = request.json
        ref_token = req_json.get("refresh")
        if not ref_token:
            return "Токен не задан", 400

        tokens = auth_service.generate_tokens(ref_token)
        if tokens:
            return tokens
        return "Ошибка в запросе", 400
