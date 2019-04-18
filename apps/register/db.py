from sqlalchemy import Column, Integer, String, TIMESTAMP

import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
engine = create_engine("sqlite:///sqlite3.db", echo=True)

# テーブル用クラス作成するとき継承
Base = declarative_base()
DataBaseSession = sessionmaker(bind=engine)


class User(Base):
    """ユーザ情報"""
    __tablename__ = 'user'

    user_id = Column(String(20), primary_key=True)  # ユーザID
    name = Column(String(255), nullable=False)
    hashed_pass_salt = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now)  # 作成日時
    updated_at = Column(TIMESTAMP, default=datetime.datetime.now)
    delete_flag = Column(Integer, default=0)


# テーブルがDBにない場合テーブルを作成
Base.metadata.create_all(engine)
