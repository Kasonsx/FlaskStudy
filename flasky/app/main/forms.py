# 表单类
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
class NameForm(Form):
	name = StringField('What is your name?', validators=[Required()])
	# validators指定一个有验证函数组合的列表，在接受用户提交的数据之前验证数据，验证函数Required()确保提交的字段不为空
	submit = SubmitField('Submit')