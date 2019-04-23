from flask import Blueprint, render_template, request, session, jsonify

from cerberus import Validator
from passlib.hash import pbkdf2_sha256

from .db import PunchClock, DataBaseSession
from sqlalchemy.orm.exc import NoResultFound
from utils.Error import CustomException

punch_app = Blueprint("punch_app", __name__, template_folder='templates', static_folder='./static')

# TODO: axiosにて送られていた打刻情報のバリデーションオブジェクト。①ユーザID, ②UTC日時、③出勤か退勤か、の情報が含まれる。
punch_validation_schema = {"user_id": {"required": True,
                                       "type": "string",
                                       "regex": r"^([0-9]|[a-z]|_){6,20}$"},
                           "password": {"required": True,
                                        "type": "string",
                                        "regex": r"^([0-9]|[a-z]|_){6,20}$"}}
punch_v = Validator(punch_validation_schema)


class Temp:
    def __init__(self, *args):
        print(args)


@punch_app.route("/punch", methods=["GET"])
def method_get():
    """現在の打刻情報をボタンに表示"""
    return render_template("punch.html")


@punch_app.route("/punch", methods=["POST"])
def method_post():
    """axiosでの打刻情報を受取る"""

    user_id = session.get("user_id")
    punching_time = request.json.get("punching_time")
    punch_in_flag = request.json.get("punch_in_flag")
    Temp(user_id)

    try:
        # 念の為、axiosにて送られてきた情報のバリデーション
        if not punch_v.validate({"punching_time": punching_time,
                                 "punch_in_flag": punch_in_flag}):
            raise CustomException

        # sqlite3ではセッションの永続化を行えないため、逐一セッションを作成する。
        db_session = DataBaseSession()

        # INSERT INTO PunchClock (user_id, punching_time, punch_in_flag) VALUES (?, ?, ?)

        db_session.close()


    except CustomException:
        pass
    except NoResultFound:
        pass

    # TODO: 返却する値は、打刻した日時、打刻の

    return jsonify(ResultSet={"test": 1})
