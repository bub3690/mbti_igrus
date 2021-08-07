#로그인 인증관련 .py 파일. app.py에서 호출한다.
import jwt
from functools import wraps
from flask import request, Response, g
from flask.json import current_app
import _app
#flask의 g는 글로벌 변수

def login_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        access_token = request.headers.get('Authorization')
        if access_token is not None:
            try:
                payload = jwt.decode(access_token,
                                     current_app.config['JWT_SECRET_KEY'],
                                     'HS256')
            except jwt.InvalidTokenError:
                payload = None

            if payload is None: return Response(status=401)

            user_id = payload['user_id']
            g.user_id = user_id
            g.user = _app.get_user(user_id) if user_id else None
        else:
            return Response(status=401)

        return f(*args,**kwargs)
    print('decorated over')
    return decorated_function
