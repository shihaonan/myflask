from flask_wtf import FlaskForm
from wtforms import TextAreaField,StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Length,DataRequired,Email,EqualTo,ValidationError
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('用户de名',validators=[DataRequired(message='请输入名户名')])
    password = PasswordField('密码', validators=[DataRequired(message='请输入密码')])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired()])
    email = StringField('邮箱',validators=[DataRequired(),Email()])
    password = PasswordField('密码',validators=[DataRequired()])
    password_confirm = PasswordField('重复密码',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('注册')

    def validate_username(self,username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError('用户名已存在')

    def validate_email(self,email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError('该邮箱已被注册')

class EditForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(message='请输入用户名')])
    about_me = TextAreaField('关于我',validators=[Length(min=0,max=140)])
    submit = SubmitField('提交')

class PostForm(FlaskForm):
    post = StringField('文章',validators=[DataRequired()])