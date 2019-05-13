from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Column, String, TIMESTAMP, DATE, INTEGER, text, TEXT, CHAR, and_

from datetime import datetime

engine = create_engine("sqlite:///sqlite3.db", echo=True)

# テーブル用クラス作成するとき継承
Base = declarative_base()
# DBとのセッションクラス
DBSession = sessionmaker(bind=engine)


# TODO: 実際は、各apps以下にModelsを定義する、が、appsを分割しすぎたせいで、同じModelを複数書くことになってしまった。DRYに反するため、リファクタリングが済むまでは暫定でこうする


class PunchClockBase(Base):
    """ユーザ情報"""
    __tablename__ = "punch_clock"
    __abstract__ = True

    user_id = Column(String(20), primary_key=True)  # ユーザID
    punched_time = Column(TIMESTAMP, nullable=False)  # 画面側で表示されている時間に合わせるため、サーバ側では値を作らない。
    delete_flag = Column(CHAR(1), default="0")
    # TODO: やっぱり、出勤/退勤の情報はレコードとして持たせない。
    punch_in_flag = Column(CHAR(1), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now)  # 作成日時
    updated_at = Column(TIMESTAMP, default=datetime.now)


class UserBase(Base):
    """ユーザ情報"""
    __tablename__ = 'user'
    __abstract__ = True

    user_id = Column(String(20), primary_key=True)  # ユーザID
    name = Column(String(255), nullable=False)
    hashed_pass_salt = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now)  # 作成日時
    updated_at = Column(TIMESTAMP, default=datetime.now)
    delete_flag = Column(CHAR(1), server_default="0")


def init_db():
    # テーブルがDBにない場合テーブルを作成
    Base.metadata.create_all(engine)
