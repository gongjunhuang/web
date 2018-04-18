from utils import log
from utils import template
from utils import redirect
from utils import http_response
from models import Todo

def index(request):
    todo_list = Todo.all()
    body = template('simple_todo_index.html', todos=todo_list)
    return http_response(body)

def edit(request):
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    body = template('simple_todo_index.html', todo=t)
    return http_response(body)

def add(request):
    """
       接受浏览器发过来的添加 todo 请求
       添加数据并发一个 302 定向给浏览器
       浏览器就会去请求 / 从而回到主页
       """
    # 得到浏览器发送的表单
    form = request.form()
    Todo.new(form)
    return redirect('/')

def update(request):
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    form = request.form()
    t.task = form.get('task')
    t.save()
    return redirect('/')

def delete(request):
    todo_id = int(request.query.get('id', -1))
    Todo.delete(todo_id)
    return redirect('/')

route_dict = {
    '/': index,
    '/add': add,
    '/edit': edit,
    '/update': update,
    '/delete': delete
}

