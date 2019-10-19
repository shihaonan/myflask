# 导入实例化的app对象
from app import app,login,db
from flask import render_template,flash,redirect,url_for,request
from app.form import LoginForm,RegisterForm,EditForm,PostForm
from flask_login import current_user,login_user,logout_user,login_required
from app.models import User, Post
from datetime import datetime
from config import config


@app.route('/')
@app.route('/<int:page>')
def index(page = 1):
    user = current_user
    users = User.query.all()
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page,config.POSTS_PER_PAGE,False)
    # posts = Post.query.paginate(1,3,False).items
    return render_template('index.html',title='首页',user=user,users = users,posts=posts)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username= form.username.data).first()
        if user is None or not user.check_pwd(form.password.data):
            flash('无效的用户名或密码')
            return redirect(url_for('login'))
        login_user(user,remember=form.remember_me.data)
        # 让登录的用户关注自己(如果没关注的话)
        if not user.is_following(user):
            db.session.add(user.follow(user))
            db.session.commit()
        flash('用户登录的用户名是：%s,是否记住我：%s'%(form.username.data,form.remember_me.data))
        return redirect(request.args.get('next') or url_for('index'))

    return render_template('login.html',title='登录',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username = form.username.data,email= form.email.data)
        user.set_pwd(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('恭喜，注册成功')
        return redirect(url_for('login'))
    return render_template('register.html',title='注册',form=form)


@app.route('/user/<username>',methods = ['GET','POST'])
@login_required
def user(username):
    form = PostForm()
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('没有'+ username + '这个用户')
        return redirect(url_for('index'))
    if form.validate_on_submit():
        post = Post(body = form.post.data,timestamp = datetime.utcnow(),author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('发表成功!')
        return redirect(url_for('user',username= current_user.username))
    posts = current_user.followed_posts().all()
    return render_template('user.html',title='这是个人中心',user=user,form=form,posts=posts)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit',methods=['GET','POST'])
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('提交成功')
        return redirect(url_for('edit'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit.html',title='个人资料编辑',form=form)


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('没有%s这个用户' % username)
        return redirect(url_for('index'))
    if user == current_user:
        flash('你不能关注自己哦')
        return redirect(url_for('user',username=username))
    u = current_user.follow(user)
    if u is None:
        flash('关注用户%s失败' % username)
        return redirect(url_for('user',username=username))
    db.session.add(u)
    db.session.commit()
    flash('成功关注了%s' % username)
    return redirect(url_for('user',username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('没有%s这个用户' % username)
        return redirect(url_for('index'))
    if user == current_user:
        flash('你不能取关自己')
        return redirect(url_for('user', username=username))
    u = current_user.unfollow(user)
    if u is None:
        flash('取关用户%s失败' % username)
        return redirect(url_for('user', username=username))
    db.session.add(u)
    db.session.commit()
    flash('你已经不再关注%s了' % username)
    return redirect(url_for('user', username=username))








