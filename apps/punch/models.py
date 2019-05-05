from sqlalchemy import Column, String, TIMESTAMP, CHAR
from sqlalchemy import and_
from datetime import datetime, timedelta
from db import Base, engine, DBSession


class PunchClock(Base):
    """ユーザ情報"""
    __tablename__ = "punch_clock"

    user_id = Column(String(20), primary_key=True)  # ユーザID
    punched_time = Column(TIMESTAMP, primary_key=True, nullable=False)  # 画面側で表示されている時間に合わせるため、サーバ側では値を作らない。
    # TODO: やっぱり、出勤/退勤の情報はレコードとして持たせない。
    punch_in_flag = Column(CHAR(1), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now)  # 作成日時
    updated_at = Column(TIMESTAMP, default=datetime.now)
    delete_flag = Column(CHAR(1), default="0")

    @classmethod
    def todays_record_exists(cls, user_id):
        """同じ日付の打刻記録が存在するか？"""

        today = datetime.now()
        # 今日の0時0分0秒
        begin_time = datetime(today.year, today.month, today.day, 0, 0, 0)
        tomorrow = datetime.now() + timedelta(days=1)
        end_time = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 0)

        db_session = DBSession()

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

        db_session.close()

        return count > 0

    @classmethod
    def insert_1_record(cls, user_id, punching_time, punch_in_flag):
        db_session = DBSession()

        # INSERT INTO PunchClock (user_id, punching_time, punch_in_flag) VALUES (?, ?, ?)
        db_session.add(PunchClock(user_id=user_id,
                                  punched_time=datetime.strptime(punching_time, '%Y/%m/%d %H:%M:%S'),
                                  punch_in_flag=punch_in_flag))
        db_session.commit()

    @classmethod
    def get_todays_attendance_record(cls, user_id):
        today = datetime.now()
        # 今日の0時0分0秒
        begin_time = datetime(today.year, today.month, today.day, 0, 0, 0)
        tomorrow = datetime.now() + timedelta(days=1)
        end_time = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 0)

        db_session = DBSession()

        # SELECT
        #   punched_time
        # FROM
        #   Punch_Clock
        # WHERE
        #   delete_flag != '1'
        # AND
        #   user_id = ?                             -- ログインしているユーザのユーザID
        # AND
        #   ? <= punched_time AND punched_time < ?  -- 今日の0時、明日の0時
        punched_times = db_session.query(PunchClock.punched_time) \
            .filter(PunchClock.delete_flag != "1") \
            .filter(PunchClock.user_id == user_id) \
            .filter(and_(begin_time <= PunchClock.punched_time,
                         PunchClock.punched_time < end_time)) \

        punched_times = [row[0] for row in punched_times]

        db_session.close()

        return punched_times


# テーブルがDBにない場合テーブルを作成
Base.metadata.create_all(engine)
