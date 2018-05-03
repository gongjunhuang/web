import time
from models import Model

class Comment(Model):
    @classmethod
    def new(cls, form):
        t = cls(form)
        t.save()
        return t

    def __init__(self, form):
        self.id = None
        self.author = form.get('author', '')
        self.content = form.get('content', '')
        self.create_time = int(time.time())