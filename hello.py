# render_template 模版
from flask import Flask, render_template
# 使用Flask-Script支持命令行选项
from flask.ext.script import Manager
app = Flask(__name__)
#manager = Manager(app)
@app.route('/')
def index():
	# return '<h1>Hello world!</h1>'
	return render_template('index.html')

@app.route('/user/<name>')
def user(name):
	# return '<h1>Hello, %s!</h1>' %name
	return render_template('user.html', name=name)

@app.route('/error')
def error():
	return '<h1>Bad Request</h1>', 400

from flask import make_response
@app.route('/response')
def response():
	response = make_response('<h1>This document carries a cookie!</h1>')
	response.set_cookie('answer', '42')
	return response

if __name__ == '__main__':
	app.run(debug=True)
	#manager.run()