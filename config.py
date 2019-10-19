class config(object):
    SECRET_KEY = 'jkljlkjkljk'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:123456@localhost:3306/myflask?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTS_PER_PAGE = 3