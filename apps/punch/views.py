from flask import Blueprint, render_template, request, session, jsonify

from cerberus import Validator

from .models import PunchClock
from db import DBSession
from sqlalchemy.orm.exc import NoResultFound
from utils.Error import CustomException
from datetime import datetime
from sqlalchemy.exc import IntegrityError
import sqlalchemy
import sqlite3

punch_app = Blueprint("punch_app", __name__, template_folder='templates', static_folder='./static')

# TODO: axiosにて送られていた打刻情報のバリデーションオブジェクト。①ユーザID, ②UTC日時、③出勤か退勤か、の情報が含まれる。
punch_validation_schema = {"user_id": {"required": True,
                                       "type": "string",
                                       "regex": r"^([0-9]|[a-z]|_){6,20}$"},
                           "punching_time": {"required": True,
                                             "type": "string",
                                             # yyyy-mm-dd hh:mm:ss の形式
                                             "regex": r"^[0-9]{4}/[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$"},
                           "punch_in_flag": {"required": True,
                                             "type": "string",
                                             "regex": r"^(0|1)$"}
                           }
punch_v = Validator(punch_validation_schema)


class Temp:
    def __init__(self, *args):
        print(args)


@punch_app.route("/punch", methods=["GET"])
def method_get():
    """現在の打刻情報をボタンに表示"""

    user_id = session.get("user_id")

    # 現在の状態が、退勤状態であるか、出勤状態であるかを確認
    # 同じ日付の押下がない == 出勤モード
    # そうでない == 退勤モード
    bool_ = PunchClock.todays_record_exists(user_id)

    # 画面上に表示するボタンのモード 0: 退勤モード 1: 出勤モード
    # 出勤モード: このモードでボタンを押下すると出勤扱いになる
    # 退勤モード: このモードでボタンを押下すると退勤扱いになる
    punch_in_flag = "0" if bool_ else "1"

    Temp(punch_in_flag)

    return render_template("punch.html", punchInFlag=punch_in_flag)


@punch_app.route("/punch", methods=["POST"])
def method_post():
    """axiosでの打刻情報を受取る"""

    user_id = session.get("user_id")
    punching_time = request.json.get("punching_time")
    punch_in_flag = request.json.get("punch_in_flag")

    is_success = False

    try:
        # 念の為、axiosにて送られてきた情報のバリデーション
        if not punch_v.validate({"user_id": user_id,
                                 "punching_time": punching_time,
                                 "punch_in_flag": punch_in_flag}):
            raise CustomException

        db_session = DBSession()

        # INSERT INTO PunchClock (user_id, punching_time, punch_in_flag) VALUES (?, ?, ?)
        db_session.add(PunchClock(user_id=user_id,
                                  punched_time=datetime.strptime(punching_time, '%Y/%m/%d %H:%M:%S'),
                                  punch_in_flag=punch_in_flag))
        db_session.commit()
        db_session.close()
        # TODO: やっぱり、レコードに退勤/出勤の情報は持たせないかも？（一旦ある程度作って操作感見てからから決める）

        is_success = True

    # TODO: ある程度出来上がったらロギングを作成する
    except CustomException as e:
        print(e)
    except sqlalchemy.orm.exc.NoResultFound as e:
        print(e)
    except sqlalchemy.exc.IntegrityError as e:
        print(e)
    except sqlite3.ProgrammingError as e:
        print(e)

    # TODO: 返却する値は、打刻した日時、打刻の

    return jsonify({"is_success": is_success,
                    "punched_time": punching_time,
                    "punch_in_flag": punch_in_flag})


@punch_app.route("/get_todays_attendance_record", methods=["GET"])
def get_todays_attendance_record():
    """当日0時 ～ 翌日0時分のレコードを取得"""
    user_id = session.get("user_id")

    punched_times = PunchClock.get_todays_attendance_record(user_id)
    # レコードが多すぎても困るので調整
    if len(punched_times) > 4:
        punched_times = punched_times[:2] + punched_times[-2:]

    return jsonify([punched_time.strftime("%Y/%m/%d %H:%M:%S")
                    for punched_time in punched_times])
