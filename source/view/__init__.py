# view를 담당함.
# view를 나누는대신, 한곳에 모음.

from flask import Flask, request, jsonify, g
from flask.json import JSONEncoder

#로그인 인증 관련

from . import auth # auth.py 파일


class CustomJSONEncoder(JSONEncoder):
    def default(self,obj):
        # 만약 set면 list로 바꿔서 리턴하고
        if isinstance(obj,set):
            return list(obj)
        # 아니면 그냥 원래 jsonencoder 사용해서 변환
        return JSONEncoder.default(self,obj)

def create_endpoints(app, services):
    app.json_encoder = CustomJSONEncoder

    user_service = services.user_service # 서비스로 전달하는 역할.
    mbti_service = services.mbti_service

    @app.route("/ping",methods=['GET'])
    def ping():
        return "pong"


    #가입 후, 호출되는 프로필 이미지 등록.
    @app.route("/profile-img-upload",methods=['POST'])
    def profile_upload():
        print(request.files)
        user_email = request.form.get('email')
        profile_img = request.files['profile_img']

        message = user_service.upload_profile(profile_email=user_email,
                       file=profile_img)

        if message.success:
            result = {'user_email': user_email, 'profile_img': profile_img.filename}
        else:
            result = {"message":message.error}
        return jsonify(result)

    @app.route("/sign-up", methods=['POST'])
    def sign_up():
        new_user    = request.json
        new_user    = user_service.create_new_user(new_user)

        return jsonify(new_user)

    @app.route('/login',methods=['POST'])
    def login():
        credential = request.json
        authorized, user_credential = user_service.login(credential)

        if authorized:
            user_id = user_credential['id']
            token = user_service.generate_access_token(user_id)

            return jsonify({
                'user_id' : user_id,
                'access_token' : token
            })
        else:
            return '',401

    @app.route("/mbti", methods=["POST"])
    @auth.login_required
    def getmbti():
         '''
         예시 데이터 구조(JSON 파일)
         {
              "E_I" : [0,0,0,0,0,0,0,0,0,0],
              "S_N" : [0,0,0,0,0,0,0,0,0,0],
              "T_F" : [0,0,0,0,0,0,0,0,0,0],
              "J_P" : [0,0,0,0,0,0,0,0,0,0]
         }
         '''

         print('글로벌 변수',g.user_id)
         user_data = request.json  # user_data는 4개의 리스트가 들어온다고 가정
         #print(user_data)
         # user_data를 함수에 넣어서 결과를 받는다.

         result = mbti_service.divideMbti(user_data) #divideMbti는 서비스로 구현.
         return result, 200
