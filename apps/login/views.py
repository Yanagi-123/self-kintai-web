from flask import Blueprint, render_template, request

from cerberus import Validator
from passlib.hash import pbkdf2_sha256

from .db import User, DataBaseSession
from sqlalchemy.orm.exc import NoResultFound
from utils.Error import CustomException


login_app = Blueprint("login_app", __name__, template_folder='templates', static_folder='./static')

login_validation_schema = {"user_id": {"required": True,
                                       "type": "string",
                                       "regex": r"^([0-9]|[a-z]|_){6,20}$"},
                           "password": {"required": True,
                                        "type": "string",
                                        "regex": r"^([0-9]|[a-z]|_){6,20}$"}}
login_v = Validator(login_validation_schema)


@login_app.route("/login", methods=["GET"])
def method_get():
    return render_template("login.html")


@login_app.route("/login", methods=["POST"])
def method_post():
    user_id = request.form.get('user_id')
    password = request.form.get('password')

    # ログイン画面に表示するエラー文字列リスト
    errors = []

    try:
        # 画面上にて入力されたユーザIDとパスワードのバリデーション
        if not login_v.validate({"user_id": user_id,
                                 "password": password}):
            raise CustomException

        # sqlite3ではセッションの永続化を行えないため、逐一セッションを作成する。
        db_session = DataBaseSession()

        # DBからハッシュ化されたパスワード文字列を取得。
        # SELECT
        #   hashed_pass_salt    -- ハッシュ化されたパスワード&ソルト
        # FROM
        #   user
        # WHERE
        #   user_id     = ?   -- 入力されたユーザID
        # AND
        #   delete_flag = '0' -- 削除されていない
        hashed_pass_salt = db_session.query(User.hashed_pass_salt) \
            .filter(User.user_id == user_id) \
            .filter(User.delete_flag == "0") \
            .one() \
            .hashed_pass_salt

        db_session.close()

        # ハッシュ化されたパスワード&ソルトと、画面側にて入力されたパスワードを照合
        if not pbkdf2_sha256.verify(password, hashed_pass_salt):
            raise CustomException

    except CustomException:
        errors.append("ログインエラー")
    except NoResultFound:
        errors.append("ログインエラー")
        return False

    return render_template("login.html", messages=errors)
