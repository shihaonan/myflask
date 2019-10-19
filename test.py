from app import db
from app.models import User,Post,followers


u=User.query.get(5)
print(u)

print('-----------------------')

# posts = Post.query.order_by(Post.timestamp.desc())
posts =Post.query.paginate(1,3,False).items
for p in posts:
    print(p.author.username,p.timestamp)

