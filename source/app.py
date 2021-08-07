from flask import Flask, request, jsonify, g

from sqlalchemy import create_engine,text


# MVC 호출
from model import UserDao
from view import create_endpoints
from service import UserService, MbtiService

#Service 클래스를 담기위해 생성
class Services:
    pass

#create app
def create_app(test_config=None):
    app=Flask(__name__)

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    database = create_engine(app.config['DB_URL'],encoding='utf-8',
                             max_overflow=0)

    ## persistence layer
    user_dao = UserDao(database)

    ## Business layer
    services = Services #객체생성
    services.user_service = UserService(user_dao,app.config)
    services.mbti_service = MbtiService()

    ## 엔드포인트들 생성

    create_endpoints(app,services)



    return app