#!/usr/bin/env python3
"""WEBアプリ起動"""
from apps.login.views import login_app
from apps.register.views import register_app

from flask import Flask, session, request, redirect

app = Flask(__name__)


@app.before_request
def before_request():
    if (  # ログイン済み
            session.get("user_id") is not None or
            # 静的ファイルに関するものの場合
            request.path.startswith("/static/") or
            # ログイン/アウト、アカウント情報作成に関するページの場合
            request.path in {"/login", "/logout", "/register"}):
        return

    # ログインされておらず，ログインページに関するリクエストでない場合
    return redirect("/login")


# ログインアプリ
app.register_blueprint(login_app)
# アカウント登録アプリ
app.register_blueprint(register_app)

if __name__ == "__main__":
    app.run(debug=True)
