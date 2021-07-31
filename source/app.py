from flask import Flask, request, jsonify, g
from flask.json import JSONEncoder,current_app
from sqlalchemy import create_engine,text
import bcrypt

import datetime
import os

#로그인 인증 관련
import jwt
import auth # auth.py 파일

#파일 업로드
from werkzeug.utils import secure_filename # 스크립트를 통해 경로를 알아내는것을 방지한다.

UPLOAD_FOLDER = '../profiles'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])




def divideMbti(user_data):
     # list 종류 E_I,S_N,T_F,J_P  각 리스트의 값이 0이면 앞, 1이면 뒤와 대응
     # ex)E_I=[1,0]면 1->I, 0->E에 대응

     E_I = user_data['E_I']
     S_N = user_data['S_N']
     T_F = user_data['T_F']
     J_P = user_data['J_P']

     # 각 선택지의 개수
     E = 0;I = 0;S = 0;N = 0;T = 0;F = 0;J = 0;P = 0;
     mbti = None # 결과를 담는 변수.

     #I,E 갯수 세기
     for j in E_I:
          if j == 0:
               E += 1
          elif j == 1:
               I += 1

     for j in S_N:
          if j == 0:
               S += 1
          elif j == 1:
               N += 1

     for j in T_F:
          if j == 0:
               T += 1
          elif j == 1:
               F += 1

     for j in J_P:
          if j == 0:
               J += 1
          elif j == 1:
               P += 1

     #최종 MBTI 결정
     if E >= I and S > N and T > F and J <= P:
          mbti = 'ESTP'
     elif E >= I and S > N and T <= F and J <= P:
          mbti = 'ESFP'
     elif E >= I and S <= N and T <= F and J <= P:
          MBTI = 'ENFP'
     elif E >= I and S <= N and T > F and J <= P:
          mbti = 'ENTP'
     elif E >= I and S > N and T > F and J > P:
          mbti = 'ESTJ'
     elif E >= I and S > N and T <= F and J > P:
          mbti = 'ESFJ'
     elif E >= I and S <= N and T <= F and J > P:
          mbti = 'ENFJ'
     elif E >= I and S <= N and T > F and J > P:
          mbti = 'ENTJ'
     elif E < I and S > N and T > F and J > P:
          mbti = 'ISTJ'
     elif E < I and S > N and T <= F and J > P:
          mbti = 'ISFJ'
     elif E < I and S <= N and T <= F and J > P:
          mbti = 'INFJ'
     elif E < I and S <= N and T > F and J > P:
          mbti = 'INTJ'
     elif E < I and S > N and T > F and J <= P:
          mbti = 'ISTP'
     elif E < I and S > N and T <= F and J <= P:
          mbti = 'ISFP'
     elif E < I and S <= N and T <= F and J <= P:
          mbti = 'INFP'
     elif E < I and S <= N and T > F and J <= P:
          mbti = 'INTP'

     return mbti

def insert_user(user):
    return current_app.database.execute(text("""
        INSERT INTO users (
            name,
            email,
            profile,
            hashed_password
        ) VALUES (
            :name,
            :email,
            :profile,
            :password
        )
    """), user).lastrowid

def get_user(user_id):
    user = current_app.database.execute(text("""
        SELECT 
            id,
            name,
            email,
            profile
        FROM users
        WHERE id = :user_id
    """), {
        'user_id' : user_id
    }).fetchone()
    return {
        'id'      : user['id'],
        'name'    : user['name'],
        'email'   : user['email'],
        'profile' : user['profile']
    } if user else None

#해싱 패스워드 확인하기위한 테스트.
def get_pass(user_mail):
    user = current_app.database.execute(text("""
            SELECT 
                email,
                id,
                hashed_password
            FROM users
            WHERE email = :user_email
        """), {
        'user_email': user_mail
    }).fetchone()
    return user


# 프로필 사진업로드. post 시에 호출되는 함수에서 다시 호출해줘야함.
# 회원가입시, 프로필 수정시 둘다 필요하기에. 분리
def upload_profile(user_email, file):
    # file = request.files['file']
    # print(file.filename)
    filename = secure_filename(file.filename)
    profile_path = UPLOAD_FOLDER+'/'+user_email
    os.makedirs(profile_path, exist_ok=True)# 각 유저마다 폴더를 만들어주기 위해. 폴더를 생성. exists_ok=True가 폴더를 만드는것.
    file.save(os.path.join(profile_path, filename))

    #db upload
    current_app.database.execute(text("""
            UPDATE users SET profile_img = :profile_path
            WHERE email=:user_email
        """),{
        'profile_path':filename,
        'user_email':user_email
    })


    return

class CustomJSONEncoder(JSONEncoder):
    def default(self,obj):
        # 만약 set면 list로 바꿔서 리턴하고
        if isinstance(obj,set):
            return list(obj)
        # 아니면 그냥 원래 jsonencoder 사용해서 변환
        return JSONEncoder.default(self,obj)


def create_app(test_config=None):
    app=Flask(__name__)
    app.json_encoder = CustomJSONEncoder
    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)
    database = create_engine(app.config['DB_URL'],encoding='utf-8',
                             max_overflow=0)
    app.database= database

    #가입 후, 호출되는 프로필 이미지 등록.
    @app.route("/profile-img-upload",methods=['POST'])
    def profile_upload():
        print(request.files)
        user_email = request.form.get('email')
        profile_img = request.files['profile_img']
        upload_profile(user_email=user_email,
                       file=profile_img)
        result = {'user_email':user_email, 'profile_img':profile_img.filename}
        return jsonify(result)

    @app.route("/sign-up", methods=['POST'])
    def sign_up():
        new_user    = request.json
        new_user['password'] = bcrypt.hashpw(
            new_user['password'].encode('UTF-8'),
            bcrypt.gensalt()
        )
        new_user_id = insert_user(new_user)
        new_user    = get_user(new_user_id)

        return jsonify(new_user)

    @app.route('/login',methods=['POST'])
    def login():
        credential = request.json
        email = credential['email']
        password = credential['password']
        row = get_pass(email)

        if row and bcrypt.checkpw(password.encode('UTF-8'),
                                  row['hashed_password'].encode('UTF-8')):
            user_id = row['id']
            payload={
                'user_id' : user_id,
                'exp':datetime.datetime.utcnow()+datetime.timedelta(seconds=60*60*24)
            }
            token = jwt.encode(payload,app.config['JWT_SECRET_KEY'])

            return jsonify({
                'access_token':token
            })
        else:
            return '존재하지않는 유저입니다. ',401


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
         result = divideMbti(user_data)
         return result, 200



    return app