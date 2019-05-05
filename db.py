from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine("sqlite:///sqlite3.db", echo=True)

# テーブル用クラス作成するとき継承
Base = declarative_base()
# DBとのセッションクラス
DBSession = sessionmaker(bind=engine)

# テーブルがDBにない場合テーブルを作成
# Base.metadata.create_all(engine)
