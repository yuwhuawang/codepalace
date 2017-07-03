#coding=utf-8
import os

from bottle import route, run, static_file, request, redirect, default_app
from bottle import jinja2_view as view

from beaker.middleware import SessionMiddleware
import uuid

sestion_opts={
    'session.type':'file',
    'session.cookei_expires': 300,
    'session.data_dir':'tmp/sessions_dir',
    'session.auto':True
}


@route("/", method="GET")
@view("template/index.html")
def hello():
    session = request.environ.get('beaker.session')
    error_msg = session.get("error_msg")
    img = session.get("img")
    username = session.get("username")
    session.pop("img")
    session.pop("error_msg")
    return {"error_msg":error_msg, "img":img, "username":username}


@route("/login", method="GET")
@view("template/login.html")
def login():
    session = request.environ.get('beaker.session')
    username = session.get("username")
    password = session.get("password")
    return {"username": username, "password": password}


@route("/login", method="POST")
def do_login():
    session = request.environ.get('beaker.session')
    username = request.forms.get("username")
    password = request.forms.get("password")
    session['username'] = username
    session['password'] = password
    if username=="yuwhuawang" and password=="wyhwyh22":
        session['login']=True
        session['username'] = username
        redirect("/")
    else:
        redirect("/login")


@route("/upload", method="POST")
def do_upload():
    session = request.environ.get('beaker.session')
    upload = request.files.get('upload')
    if not upload:
        session['error_msg'] = u"请选择图片后点击上传"
    else:
        name, ext = os.path.splitext(upload.filename)
        if ext not in(".jpg", ".jpeg"):
            session['error_msg'] = u"图片格式不正确"
        else:
            file_name = str(uuid.uuid4())+upload.filename
            save_path = os.path.join('imgs',file_name)
            upload.save(save_path)
            session['img'] = file_name
    redirect("/")


@route("/assets/<filepath:path>")
def server_static(filepath):
    return static_file(filepath, root="template/assets")

@route("/imgs/<filepath:path>")
def server_static(filepath):
    return static_file(filepath, root="imgs")

dapp = default_app()
session_app = SessionMiddleware(dapp,sestion_opts)

run(session_app,host='localhost', port=9000, debug=True)