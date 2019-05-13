#!/usr/bin/env python3
from flask import Blueprint, render_template, session, request, redirect, url_for
from sqlalchemy.exc import IntegrityError
from cerberus import Validator
from passlib.hash import pbkdf2_sha256
from .models import User, DataBaseSession
from utils.Error import CustomException

register_app = Blueprint("register_app", __name__, template_folder='templates', static_folder='./static')

register_validation_schema = {"user_id": {"required": True,
                                          "type": "string",
                                          "regex": r"^([0-9]|[a-z]|_){4,20}$"},
                              "password": {"required": True,
                                           "type": "string",
                                           "regex": r"^([0-9]|[a-z]|_){4,20}$"},
                              "name": {"required": False,
                                       "type": "string",
                                       "nullable": True}}

register_v = Validator(register_validation_schema)

# TODO; login, logout, registerは全て「auth」ディレクトリを作って統合


@register_app.route("/register", methods=["GET"])
def method_get():
    """アカウント画面に遷移した場合の処理"""
    return render_template("register.html")


@register_app.route("/register", methods=["POST"])
def method_post():
    """アカウント登録画面にて、登録ボタンが押下された場合の処理"""
    user_id = request.form.get('user_id')
    password = request.form.get('password')
    name = request.form.get("name")

    # アカウント登録画面に表示するエラー文字列リスト
    errors = []
    try:
        # 画面にて入力された、ユーザID、パスワード、名前のバリデーション
        if not register_v.validate({"user_id": user_id,
                                    "password": password,
                                    "name": name}):
            raise CustomException

        # パスワードからハッシュとソルトが結合された文字列を生成。
        # 文字列の形式: $pbkdf2-{digest}${rounds}${salt}${checksum}
        hashed_pass_salt = pbkdf2_sha256.hash(password)
        # sqlite3ではセッションの永続化を行えないため、逐一セッションを作成する。
        db_session = DataBaseSession()

        # INSERT INTO user (
        #   user_id,            -- ユーザID
        #   name,               -- 名前
        #   hashed_pass_salt    -- ハッシュ化したパスワード&ソルト
        #   )
        # VALUES (?, ?, ?)
        db_session.add(User(user_id=user_id, name=name, hashed_pass_salt=hashed_pass_salt))

        db_session.commit()
        db_session.close()

    except CustomException:
        errors.append("アカウントに使用できない文字列が含まれています。")
    except IntegrityError:
        errors.append("このユーザIDは既に使用されています。別のユーザIDを選択してください。")

    if errors:
        return render_template("register.html", messages=errors)
    else:
        session['user_id'] = user_id
        return redirect(url_for('punch_app.method_get'))


