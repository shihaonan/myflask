from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from hashlib import md5

if __name__ == '__main__':
    db.metadata.clear()

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))

class User(db.Model,UserMixin):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64),index = True,unique = True)
    email = db.Column(db.String(120),unique = True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post',backref='author',lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship('User',
                               secondary = followers,
                               primaryjoin = (followers.c.follower_id == id),
                               secondaryjoin = (followers.c.followed_id == id),
                               backref = db.backref('followers',lazy = 'dynamic'),
                               lazy = 'dynamic')

    def set_pwd(self,pwd):
        self.password_hash = generate_password_hash(pwd)

    def check_pwd(self,pwd):
        return check_password_hash(self.password_hash,pwd)

    def __repr__(self):
        return '<打印用户名: %r>' % (self.username)

    def avatar(self,size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/%s?d=identicon&s=%s' % (digest,size)

    def follow(self,user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self,user):
        self.followed.remove(user)
        return self

    def is_following(self,user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        return Post.query.join(followers,
                               (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id).order_by(Post.timestamp.desc())



class Post(db.Model):
    __tablename__ = 'post'
    __table_args__ = {'extend_existing': True}
    id= db.Column(db.Integer,primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime,default=datetime.utcnow())
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %s>' %(self.body)

