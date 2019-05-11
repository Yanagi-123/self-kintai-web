from sqlalchemy import Column, String, TIMESTAMP, DATE, INTEGER, text, TEXT
from jinjasql import JinjaSql

from datetime import datetime, timedelta, date

from db import Base, engine, DBSession
import calendar


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


# テーブルがDBにない場合テーブルを作成
Base.metadata.create_all(engine)
