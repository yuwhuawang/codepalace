#coding=utf-8
import os

from bottle import route, run, static_file, request, redirect, default_app
from bottle import jinja2_view as view

from beaker.middleware import SessionMiddleware

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
    session.clear()
    return {"error_msg":error_msg, "img":img}


@route("/upload", method="POST")
def do_upload():
    session = request.environ.get('beaker.session')
    upload = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    if ext not in(".jpg", ".jpeg"):
        session['error_msg'] = u"图片格式不正确"
    else:
        save_path = os.path.join('imgs', upload.filename)
        upload.save(save_path)
        session['img'] = upload.filename
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