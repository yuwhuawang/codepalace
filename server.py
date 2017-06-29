#coding=utf-8
from bottle import route, run, static_file
from bottle import jinja2_view as view

@route("/")
@view("template/index.html")
def hello():
    pass

@route("/assets/<filepath:path>")
def server_static(filepath):
    return static_file(filepath, root="template/assets")

run(host='localhost', port=9000, debug=True)