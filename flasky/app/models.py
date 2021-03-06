# 使用Werkzeug实现密码散列
from werkzeug.security import generate_password_hash, check_password_hash
# generate_password_hash(password,method,salt_length)输出密码的散列值
# check_password_hash(hash,password)验证密码和散列值，正确返回True
from flask.ext.login import UserMixin
from . import db, login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

# 定义Role和User模型
class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	users = db.relationship('User', backref='role')
	#backref在关系的另一个模型中添加反向引用

	def __repr__(self):
		return '<Role %r>' %self.name
class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True, index=True)
	username = db.Column(db.String(64), unique=True, index=True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	password_hash = db.Column(db.String(128))
	confirmed = db.Column(db.Boolean, default=False)

	def generate_confirmation_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		retunr s.dumps({'confirm':self.id})
	

	@property
	def password(self):
		raise AttributeError('Password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User %r>' % self.username

@login_manager.user_loader
def load_uesr(user_id):
	return User.query.get(int(user_id))