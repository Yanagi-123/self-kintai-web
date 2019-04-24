from sqlalchemy import Column, Integer, String, TIMESTAMP, CHAR

import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine("sqlite:///sqlite3.db", echo=True)

# テーブル用クラス作成するとき継承
Base = declarative_base()
DataBaseSession = sessionmaker(bind=engine)


class PunchClock(Base):
    """ユーザ情報"""
    __tablename__ = "punch_clock"

    user_id = Column(String(20), primary_key=True)  # ユーザID
    punched_time = Column(TIMESTAMP, primary_key=True, nullable=False)  # 画面側で表示されている時間に合わせるため、サーバ側では値を作らない。
    punch_in_flag = Column(CHAR(1), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now)  # 作成日時
    updated_at = Column(TIMESTAMP, default=datetime.datetime.now)
    delete_flag = Column(CHAR(1), default="0")


# テーブルがDBにない場合テーブルを作成
Base.metadata.create_all(engine)
