from flask import Blueprint, render_template, request, session, jsonify

from cerberus import Validator

from .db import PunchClock, DataBaseSession
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound
from utils.Error import CustomException
from datetime import datetime, timedelta

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

    today = datetime.now()
    begin_time = datetime(today.year, today.month, today.day, 0, 0, 0)
    tomorrow = datetime.now() + timedelta(days=1)
    end_time = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 0)

    # sqlite3ではセッションの永続化を行えないため、逐一セッションを作成する。
    db_session = DataBaseSession()

    # 現在の状態が、退勤状態であるか、出勤状態であるかを確認
    # 同じ日付の押下がない == 出勤モード
    # そうでない == 退勤モード
    # SELECT
    #   COUNT(*)
    # FROM
    #   PunchClock
    # WHERE
    #   user_id = ?             -- ログインしているユーザのユーザID
    # AND
    #   ? <= punched_time < ?   -- 今日の0時、明日の0時
    count = db_session.query(PunchClock.user_id) \
        .filter(PunchClock.user_id == user_id) \
        .filter(and_(begin_time <= PunchClock.punched_time,
                     PunchClock.punched_time < end_time)) \
        .count()

    # 0: 退勤モード 1: 出勤モード
    punch_in_flag = "0" if count else "1"

    Temp(punch_in_flag)

    db_session.close()
    return render_template("punch.html", punchInFlag=punch_in_flag)


@punch_app.route("/punch", methods=["POST"])
def method_post():
    """axiosでの打刻情報を受取る"""

    user_id = session.get("user_id")
    punching_time = request.json.get("punching_time")
    punch_in_flag = request.json.get("punch_in_flag")
    Temp(user_id)
    json = {}

    try:
        # 念の為、axiosにて送られてきた情報のバリデーション
        if not punch_v.validate({"user_id": user_id,
                                 "punching_time": punching_time,
                                 "punch_in_flag": punch_in_flag}):
            raise CustomException

        # sqlite3ではセッションの永続化を行えないため、逐一セッションを作成する。
        db_session = DataBaseSession()

        # INSERT INTO PunchClock (user_id, punching_time, punch_in_flag) VALUES (?, ?, ?)
        db_session.add(PunchClock(user_id=user_id,
                                  punched_time=datetime.strptime(punching_time, '%Y/%m/%d %H:%M:%S'),
                                  punch_in_flag=punch_in_flag))
        db_session.commit()

        json = {"is_success": True,
                "punched_time": punching_time,
                "status": 1}

        db_session.close()

    except CustomException:
        pass
    except NoResultFound:
        pass

    # TODO: 返却する値は、打刻した日時、打刻の

    return jsonify(json)
