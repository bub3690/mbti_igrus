import bcrypt
import jwt
import datetime
import os
#파일 업로드
from werkzeug.utils import secure_filename # 스크립트를 통해 경로를 알아내는것을 방지한다.
UPLOAD_FOLDER = '../profiles'



class UserService:
    def __init__(self,user_dao,config):
        self.user_dao = user_dao
        self.config = config
        # DAO(Data Access Object)는 DB를 사용해 데이터를 조회하거나 조작하는 기능을 전담
        # persistence layer에 의존.

    def create_new_user(self,new_user):
        new_user['password'] = bcrypt.hashpw(
            new_user['password'].encode('UTF-8'),
            bcrypt.gensalt()
        )

        # user_dao를 통해 persistance layer로 넘긴다.
        new_user_id = self.user_dao.insert_user(new_user)
        new_user    = self.user_dao.get_user(new_user_id)

        return new_user

    def login(self,credential):
        email   = credential['email']
        password = credential['password']
        user_credential = self.user_dao.get_pass(email)
        authorized = user_credential and bcrypt.checkpw(
            password.encode('UTF-8'),
            user_credential['hashed_password'].encode('UTF-8')
        )

        return authorized,user_credential



    def generate_access_token(self,user_id):
        payload = {
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60 * 24)
        }
        token = jwt.encode(payload, self.config['JWT_SECRET_KEY'])
        #config는 self안에 있는것으로 수정.

        return token

    def upload_profile(self, profile_email,file):
        # profile_email은 user_email과 같은것.
        try:
            filename = secure_filename(file.filename)
            profile_path = UPLOAD_FOLDER + '/' + profile_email
            os.makedirs(profile_path, exist_ok=True)  # 각 유저마다 폴더를 만들어주기 위해. 폴더를 생성. exists_ok=True가 폴더를 만드는것.
            file.save(os.path.join(profile_path, filename))

            #db upload
            self.user_dao.profile_upload(profile_path,profile_email)

        except Exception as e:
            print(e)
            return {"success":False,"error":e}
