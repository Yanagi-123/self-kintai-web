from flask import Blueprint, session, render_template, request, jsonify
from .models import UserInput
from datetime import datetime

attendance_app = Blueprint("attendance_app", __name__, template_folder='templates', static_folder='./static')


# TODO: アプリのメソッド名とかはrestに合わせることにする

@attendance_app.route("/attendance", methods=["GET"])
def method_get():
    user_id = session.get("user_id")
    today = datetime.now()
    year = today.year
    month = today.month
    records = UserInput.aaa(user_id, year, month)

    attendances = [{"date": date_,
                    "punched_in_time": punched_in_time,
                    "punched_out_time": punched_out_time,
                    "break_time": break_time,
                    "note": note}
                   for date_, punched_in_time, punched_out_time, break_time, note in records]

    return render_template("attendance.html", attendances=attendances)


@attendance_app.route("/attendance/get", methods=["GET"])
def get_attendance():
    # TODO: ここで形式チェックも行う
    user_id = session.get("user_id")

    year = int(request.args.get("year"))
    month = int(request.args.get("month"))

    records = UserInput.aaa(user_id, year, month)

    def func(tuple_):

        date_, punched_in_time, punched_out_time, break_time, note = tuple_

        # TODO: ここで形式チェックも行う
        # TODO: ノーマライズもサーベラスで行うかも
        date_ = date_[5:]
        if punched_in_time:
            punched_in_time = datetime.strptime(punched_in_time,
                                                '%Y-%m-%d %H:%M:%S.%f').strftime("%H:%M")
        else:
            punched_in_time = ""

        if punched_out_time:
            punched_out_time = datetime.strptime(punched_out_time,
                                                 '%Y-%m-%d %H:%M:%S.%f').strftime("%H:%M")
        else:
            punched_out_time = ""

        if break_time:
            break_time = break_time
        else:
            break_time = ""

        if not note:
            note = ""

        return {"date": date_,
                "punched_in_time": punched_in_time,
                "punched_out_time": punched_out_time,
                "break_time": break_time,
                "note": note}

    attendances = [func(tuple_) for tuple_ in records]

    return jsonify(attendances)


@attendance_app.route("/attendance/put", methods=["POST"])
def put_attendance():
    # TODO: 取得した値の形式チェックを行う
    user_id = session.get("user_id")
    items = request.json

    records = UserInput.bbb(user_id, items)

    return "test"
