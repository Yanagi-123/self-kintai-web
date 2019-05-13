#!/usr/bin/env python3
"""WEBアプリ起動"""
import random
import string

from apps.login.views import login_app
from apps.register.views import register_app
from apps.punch.views import punch_app
from apps.attendance.views import attendance_app
from apps.index.views import index_app

from flask import Flask, session, request, redirect

from db import init_db

init_db()

app = Flask(__name__)


@app.before_request
def before_request():
    if (  # ログイン済み
            session.get("user_id") is not None or
            # 静的ファイルに関するものの場合
            request.path.startswith("/static/") or
            # ログイン/アウト、アカウント情報作成に関するページの場合
            request.path in {"/", "/login", "/logout", "/register"}):
        return

    # ログインされておらず，ログインページに関するリクエストでない場合
    return redirect("/login")


# トップ画面（機能紹介等）
app.register_blueprint(index_app)
# ログインアプリ
app.register_blueprint(login_app)
# アカウント登録アプリ
app.register_blueprint(register_app)
# 打刻登録アプリ
app.register_blueprint(punch_app)
# 打刻修正画面
app.register_blueprint(attendance_app)

if __name__ == "__main__":
    # app.secret_key = ''.join(random.sample(string.printable, k=50))
    app.secret_key = 'a'
    app.run(debug=True)
