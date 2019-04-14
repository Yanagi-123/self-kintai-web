#!/usr/bin/env python3

from flask import Flask, session
from apps.login.views import login_app

from flask import request, redirect

app = Flask(__name__)


@app.before_request
def before_request():
    if (  # ログイン済み
            session.get("user_id") is not None or
            # 静的ファイルに関するものの場合
            request.path.startswith("/static/") or
            # ログインに関するページの場合
            request.path in {"/login", "/logout", "/register"}):
        return

    # ログインされておらず，ログインページに関するリクエストでない場合
    return redirect("/login")


app.register_blueprint(login_app)

if __name__ == "__main__":
    app.run(debug=True)
