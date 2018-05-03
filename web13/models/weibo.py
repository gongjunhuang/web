from models import Model
from models.user import User

class Weibo(Model):
    def __init__(self, form, user_id=-1):
        self.id = form.get('id', None)
        self.content = form.get('content', '')
        self.user_id = form.get('user_id', user_id)

    def comments(self):
        return Comment.find_all(weibo_id=self.id)

class Comment(Model):
    def __init__(self, form, user_id=-1):
        self.id = form.get('id', None)
        self.content = form.get('content', '')
        self.user_id = form.get('user_id', user_id)
        self.weibo_id = form.get('weibo_id', -1)

    def user(self):
        u = User.find_by(id=self.user_id)
        return u