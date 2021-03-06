# render_template 模版
from flask import Flask, render_template
app = Flask(__name__)
# 使用Flask-Script支持命令行选项
from flask.ext.script import Manager
manager = Manager(app)
# 设置Flask-WTF
app.config['SECRET_KEY'] = 'hard to guess string'
# 配置数据库
from flask.ext.sqlalchemy import SQLAlchemy
import os
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
# 使用Bootstrap模版
from flask.ext.bootstrap import Bootstrap
bootstrap = Bootstrap(app)

from flask.ext.moment import Moment
moment = Moment(app)

from datetime import datetime
from flask import session, redirect, url_for, flash
# 重定向和用户会话
# flash 消息
@app.route('/', methods=['GET', 'POST'])
def index():
	# return '<h1>Hello world!</h1>'
	form = NameForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.name.data).first()
		if user is None:
			user = User(username = form.name.data)
			db.session.add(user)
			session['known'] = False
		else:
			session['known'] = True
		session['name'] = form.name.data
		form.name.data = ''
		return redirect(url_for('index'))
	return render_template('index.html', form=form, name=session.get('name'), known=session.get('known', False))

	# if form.validate_on_submit():
	# 	old_name = session.get('name')
	# 	if old_name is not None and old_name != form.name.data:
	# 		flash('Looks like you have changed your name!')
	# 	session['name'] = form.name.data
	# 	return redirect(url_for('index'))
	# return render_template('index.html', form=form, name=session.get('name'), current_time=datetime.utcnow())

@app.route('/user/<name>')
def user(name):
	# return '<h1>Hello, %s!</h1>' %name
	return render_template('user.html', name=name)

@app.route('/error')
def error():
	return '<h1>Bad Request</h1>', 400

@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500

from flask import make_response
@app.route('/response')
def response():
	response = make_response('<h1>This document carries a cookie!</h1>')
	response.set_cookie('answer', '42')
	return response

# 表单类
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
class NameForm(Form):
	name = StringField('What is your name?', validators=[Required()])
	# validators指定一个有验证函数组合的列表，在接受用户提交的数据之前验证数据，验证函数Required()确保提交的字段不为空
	submit = SubmitField('Submit')

# 定义Role和User模型
class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	users = db.relationship('User', backref='role')
	#backref在关系的另一个模型中添加反向引用

	def __repr__(self):
		return '<Role %r>' %self.name
class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

	def __repr__(self):
		return '<User %r>' % self.username

# 集成Python Shell,为Shell命令添加一个上下文
from flask.ext.script import Shell
def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role)
	# 注册程序、数据库实例以及模型
manager.add_command("shell", Shell(make_context=make_shell_context))

from flask.ext.migrate import Migrate, MigrateCommand
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	app.run(debug=True)
	manager.run()