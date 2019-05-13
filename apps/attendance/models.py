from sqlalchemy import Column, String, TIMESTAMP, DATE, INTEGER, text, TEXT, CHAR, and_
from jinjasql import JinjaSql

from datetime import datetime, timedelta, date

from db import Base, engine, DBSession, PunchClockBase
import calendar

Base.metadata.clear()


class PunchClock(PunchClockBase):
    """ユーザ情報"""
    pass


class UserInput(Base):
    """ユーザ情報"""
    __tablename__ = 'user_input'
    user_id = Column(String(20), primary_key=True)  # ユーザID
    date_on_calender = Column(DATE, primary_key=True)  # ユーザID
    break_time = Column(INTEGER)  # ユーザID
    note = Column(TEXT)  # ユーザID
    created_at = Column(TIMESTAMP, default=datetime.now)  # 作成日時
    updated_at = Column(TIMESTAMP, default=datetime.now)

    @classmethod
    def aaa(cls, user_id, year, month):
        # TODO:postgresqlを使用する場合は、generate_seriesで置換できる
        # TODO: クエリは外だし
        template = r"""
        WITH
          dates AS (
            {% for date_  in dates %}
            SELECT {{date_}} AS date_
            {% if not loop.last %}
            UNION ALL
            {% endif %}
            {% endfor %}
          )
        , punch AS (
            SELECT
              DATE(punched_time)    AS date_
            , MIN(punched_time)     AS punched_in_time
            , CASE
                WHEN COUNT(punched_time) = 1 THEN NULL
                ELSE MAX(punched_time)
              END                   AS punched_out_time
            FROM
              punch_clock
            WHERE
              delete_flag != '1'
            AND
              user_id = {{user_id}}
            GROUP BY
              date_
            ORDER BY
              date_ ASC
          )
         , input AS (
            SELECT
              date_on_calender AS date_
            , break_time
            , note
            FROM
              user_input
            WHERE
              user_id = 'user_000000'
        )
        SELECT
          t_d.date_
        , t_p.punched_in_time
        , t_p.punched_out_time
        , t_i.break_time
        , t_i.note
        FROM
          dates AS t_d
        LEFT JOIN
          punch AS t_p
          ON t_d.date_ = t_p.date_
        LEFT JOIN
          input AS t_i
          ON t_d.date_ = t_i.date_
        """
        # 指定された月の日数
        _, days_num = calendar.monthrange(year, month)
        # 指定された月の日付リスト（yyyy-mm-ddの形式）
        dates = [(date(year, month, 1) + timedelta(days=idx)).strftime("%Y-%m-%d")
                 for idx in range(days_num)]
        # 値をバインドする際、1:, 2: の形式にする
        j = JinjaSql(param_style='numeric')
        # 実行するクエリ、バインドする値
        query, params = j.prepare_query(template, {"dates": dates,
                                                   "user_id": user_id})
        # sqlalchemyの仕様上、値をバインドする際はキー情報が必要なため付加
        bind_params = {f"{idx + 1}": date_ for idx, date_ in enumerate(params)}

        db_session = DBSession()

        result = db_session.execute(text(query), bind_params)
        records = [(date_, punched_in_time, punched_out_time, break_time, note)
                   for date_, punched_in_time, punched_out_time, break_time, note in result]

        db_session.close()

        return records

    @classmethod
    def bbb(cls, user_id, items):

        records = items.get("records")
        year = items.get("year")

        db_session = DBSession()

        def func_1(date_, punched_in_time, punched_out_time):
            # TODO: やっぱり、画面に初期表示した時点で、どういう状態だったか？をフロント側で持たせる。
            # TODO: 元々入力されてたけど、やっぱり空になった場合を考える。

            count = db_session.query(PunchClock) \
                .filter(PunchClock.user_id == user_id)

            if punched_in_time == "":
                return

            punched_in_time = datetime.strptime(f"{year}-{date_} {punched_in_time}:00", "%Y-%m-%d %H:%M:%S")
            # SELECT
            #   COUNT(*)
            # FROM
            #   Punch_Clock
            # AND
            #   user_id = 'user_000000'
            # AND
            #   punched_time == '2019-05-01 00:00:00.000000'
            count = db_session.query(PunchClock) \
                .filter(PunchClock.user_id == user_id) \
                .filter(PunchClock.punched_time == punched_in_time) \
                .count()

            if count:
                result = db_session.query(PunchClock) \
                    .filter(PunchClock.user_id == user_id) \
                    .filter(PunchClock.punched_time == punched_in_time) \
                    .first()
                result.delete_flag = '0'
                db_session.commit()

                return

            # UPDATE
            #   Punch_Clock
            # SET
            #   delete_flag = '1'
            # WHERE
            #   user_id = ?
            # AND
            #   punched_time IN (
            #     SELECT
            #       punched_time
            #     FROM
            #       Punch_Clock
            #     WHERE
            #       delete_flag != '1'
            #     AND
            #       -- 例）?: 'user_1'
            #       user_id = ?
            #     AND
            #       -- 例）?: '2019-01-01 07:30:00.000000'
            #       punched_time != ?
            #     AND
            #       -- 例）?: 2019-01-01、?: 2019-01-02
            #       ? <= punched_time AND punched_time < ?
            #     AND
            #       -- 入力された時間
            #       punched_time < ?
            #   )
            result = db_session.query(PunchClock) \
                .filter(PunchClock.delete_flag != "1") \
                .filter(PunchClock.user_id == user_id) \
                .filter(PunchClock.user_id != punched_in_time) \
                .filter(and_(punched_in_time.date() <= PunchClock.punched_time,
                             PunchClock.punched_time < punched_in_time.date() + timedelta(days=1))) \
                .filter(PunchClock.punched_time < punched_in_time)

            for row in result:
                row.delete_flag = '1'

            db_session.add(PunchClock(user_id=user_id,
                                      punched_time=punched_in_time,
                                      punch_in_flag='1'))
            db_session.commit()

        # punchテーブル
        # 1. 画面上から取得した内容で検索して、違うレコードを抽出
        # 2. 全部空のレコードを排除
        # 3. まだレコードが存在してたらDB処理に
        # 4. 出勤時間に関しては、入力された時間より小さいレコードの有効フラグを無効化し、新しいレコードをINSERT
        # 5. 退勤時間に関しては、入力された時間より大きいレコードの有効フラグを無効化し、新しいレコードをINSERT

        # user_inputテーブル
        # 1. 画面上から取得した内容で検索して、違うレコードを抽出
        # 2. 全部空のレコードを排除
        # 3. UPDATE
        for dict_ in records:
            date_ = dict_["date"]
            punched_in_time = dict_["punched_in_time"]
            punched_out_time = dict_["punched_in_time"]
            func_1(date_, punched_in_time, punched_out_time)

        return []


# テーブルがDBにない場合テーブルを作成

Base.metadata.create_all(engine)
