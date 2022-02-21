#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import Flask, request, render_template, redirect

from api import insert, update, delete, select

app = Flask(__name__)
app.key = "super secret key"


@app.route("/", methods=["GET"])
def index():
    user_status = True if select("User", condition=f"user_id=\'{request.cookies.get('user_id')}\'") else False
    user_config = False
    user_bind = False
    if user_status:
        user_config = select("Config", condition=f"id=(select id from User where user_id=\'{request.cookies.get('user_id')}\')")
        user_bind = select("Bind", condition=f"id=(select id from User where user_id=\'{request.cookies.get('user_id')}\')")
    return render_template("index.html", user=user_status, user_config=user_config, user_bind=user_bind)


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    match request.method:
        case "POST":
            try:
                insert(f'\'{request.form.get("user_id")}\'', "User", column="user_id")
                resp = redirect("/")
                resp.set_cookie("user_id", request.form.get("user_id"), max_age=86400, path="/")
                return resp
            except Exception:
                return render_template("registration.html", title="CS:GO|Sign up", error="ID is busy! Please create another ID")
        case "GET":
            return render_template("registration.html", title="CS:GO|Sign up", error=False)


@app.route("/sign_in", methods=["GET"])
def sign_in():
    user_status = True if select("User", condition=f"user_id=\'{request.cookies.get('user_id')}\'") else False
    if user_status:
        return redirect("/")
    else:
        if request.args:
            check = True if len(select("User", condition=f"user_id=\'{request.args.get('user_id')}\'"))==1 else False
            if check:
                resp = redirect("/")
                resp.set_cookie("user_id", request.args.get('user_id'), max_age=86400, path="/")
                return resp
            else:
                return render_template("sign.html", title="CS:GO|Sign in", error="ID is invalid! Try again!")
        else:
            return render_template("sign.html", title="CS:GO|Sign in", error=False)


@app.route("/account", methods=["GET", "POST"])
def profile():
    user_status = True if select("User", condition=f"user_id=\'{request.cookies.get('user_id')}\'") else False
    match request.method:
        case "POST":
            page = redirect('/')
            page.delete_cookie("user_id", path="/")
            return page
        case "GET":
            if user_status:
                user = select("User", condition=f"user_id=\'{request.cookies.get('user_id')}\'")[0]
                return render_template("profile.html", title="CS:GO|Profile", profile=user, user=user_status)
            else:
                return redirect('/')


@app.route("/config", methods=["GET", "POST"])
def add_or_get_config():
    user_status = True if select("User", condition=f"user_id=\'{request.cookies.get('user_id')}\'") else False
    configs = select("Config", condition=f"id=(select id from User where user_id=\'{request.cookies.get('user_id')}\')")
    match request.method:
        case 'POST':
            if request.form.get("config_code"):
                try:
                    insert(f"(select id from User where user_id='{request.cookies.get('user_id')}'), (select count(position) from Config where id=(select id from User where user_id='{request.cookies.get('user_id')}')), '{request.form.get('config_name')}', '{request.form.get('config_code')}'", "Config")
                    configs_new = select("Config", condition=f"id=(select id from User where user_id=\'{request.cookies.get('user_id')}\')")
                    return render_template("config.html", title="CS:GO|Config", error=False, user_config=configs_new, user=user_status)
                except Exception:
                    return render_template("config.html", title='CS:GO|Config', error="Error!", user_config=configs, user=user_status)
            elif request.form.get("delete"):
                try:
                    delete("Config", condition=f"position={request.form.get('delete')}")
                    configs_new = select("Config", condition=f"id=(select id from User where user_id=\'{request.cookies.get('user_id')}\')")
                    return render_template("config.html", title="CS:GO|Config", error=False, user_config=configs_new, user=user_status)
                except Exception:
                    return render_template("config.html", title='CS:GO|Config', error="Error!", user_config=configs, user=user_status)
            else:
                return render_template("config.html", title='CS:GO|Config', error="Bad value!", user_config=configs, user=user_status)
        case 'GET':
            return render_template("config.html", title="CS:GO|Config", error=False, user_config=configs, user=user_status)


@app.route("/bind", methods=["GET", "POST"])
def add_or_get_bind():
    user_status = True if select("User", condition=f"user_id=\'{request.cookies.get('user_id')}\'") else False
    binds = select("Bind", condition=f"id=(select id from User where user_id=\'{request.cookies.get('user_id')}\')")
    match request.method:
        case 'POST':
            if request.form.get("bind_code"):
                try:
                    insert(f"(select id from User where user_id='{request.cookies.get('user_id')}'), (select count(position) from Bind where id=(select id from User where user_id='{request.cookies.get('user_id')}')), '{request.form.get('bind_name')}', '{request.form.get('bind_code')}'", "Bind")
                    binds_new = select("Bind", condition=f"id=(select id from User where user_id=\'{request.cookies.get('user_id')}\')")
                    return render_template("bind.html", title="CS:GO|Bind", error=False, user_bind=binds_new, user=user_status)
                except Exception as err:
                    return render_template("bind.html", title='CS:GO|Bind', error="Error!", user_bind=binds, user=user_status)
            elif request.form.get("delete"):
                try:
                    delete("Bind", condition=f"position={request.form.get('delete')}")
                    binds_new = select("Bind", condition=f"id=(select id from User where user_id=\'{request.cookies.get('user_id')}\')")
                    return render_template("bind.html", title='CS:GO|Bind', error=False, user_bind=binds_new, user=user_status)
                except Exception:
                    return render_template("bind.html", title='CS:GO|Bind', error="Error!", user_bind=binds, user=user_status)
        case 'GET':
            return render_template("bind.html", title="CS:GO|Bind", error=False, user_bind=binds, user=user_status)


@app.route("/search", methods=["GET"])
def search():
    user_status = True if select("User", condition=f"user_id=\'{request.cookies.get('user_id')}\'") else False
    configs = select("Config", condition=f"name=\'{request.args.get('search')}\'")
    binds = select("Bind", condition=f"name=\'{request.args.get('search')}\'")
    return render_template("search.html", title="CS:GO|Search", user_config=configs, user_bind=binds, user=user_status)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
