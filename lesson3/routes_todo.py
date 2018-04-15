'''
点击添加按钮增加一个新的 todo 的时候, 程序的流程如下(包含原始 HTTP 报文)
    1, 浏览器提交一个表单给服务器(发送 POST 请求)
POST /todo/add HTTP/1.1
Content-Type: application/x-www-form-urlencoded

title=heuv
    2, 服务器解析出表单的数据, 并且增加一条新数据, 并返回 302 响应
HTTP/1.1 302 REDIRECT
Location: /todo

    3, 浏览器根据 302 中的地址, 自动发送了一条新的 GET 请求
GET /todo HTTP/1.1
Host: ....

    4, 服务器给浏览器一个页面响应
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: ...

<html>
    ....
</html>
    5, 浏览器把新的页面显示出来

'''

from utils import log
from todo import Todo
from models import User
from routes import current_user

def template(name):
    # 根据名字读取template文件夹中的一个文件并返回
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def response_with_headers(headers, code=200):
    """
        Content-Type: text/html
        Set-Cookie: user=gua
        """
    header = 'HTTP/1.1 {} VERY OK\r\n'.format(code)
    header += ''.join('{}: {}\r\n'.format(k, v) for k, v in headers.items())
    return header

def redirect(url):
    """
    浏览器在收到 302 响应的时候
    会自动在 HTTP header 里面找 Location 字段并获取一个 url
    然后自动请求新的 url
    """
    headers = {
        'Location': url,
    }
    r = response_with_headers(headers, 302) + '\r\n'
    return r.encode('utf-8')

def login_required(route_function):
    def f(request):
        uname = current_user(request)
        u = User.find_by(username=uname)
        if u is None:
            return redirect('/login')
        return route_function(request)
    return f

def index(request):
    headers = {
        'Content-Type': 'text/html'
    }
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    todo_list = Todo.find_all(user_id=u.id)
    # 下面这行生成一个 html 字符串
    # todo_html = ''.join(['<h3>{} : {} </h3>'.format(t.id, t.title)
    #                      for t in todo_list])
    # 上面一行列表推倒的代码相当于下面几行
    todos = []
    for t in todo_list:
        edit_link = '<a href="/todo/edit?id={}">编辑</a>'.format(t.id)
        delete_link = '<a href="/todo/delete?id={}">删除</a>'.format(t.id)
        s = '<h3>{} : {} {} {}</h3>'.format(t.id, t.title, edit_link, delete_link)
        todos.append(s)
    todo_html = ''.join(todos)
    #替换模板中的标记字符串
    body = template('todo_index.html')
    body = body.replace('{{todos}}', todo_html)
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')

def edit(request):
    headers = {
        'Content-Type': 'text/html'
    }
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    if t.user_id != u.id:
        return redirect('/login')
    body = template('tody_edit.html')
    body = body.replace('{{todo_id}}', str(t.id))
    body = body.replace('{{todo_title}}', str(t.title))
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')

def add(request):
    headers = {
        'Content-Type': 'text/html'
    }

    uname = current_user(request)
    u = User.find_by(username=uname)
    if request.method == 'POST':
        form = request.form()
        t = Todo.new(form)
        t.user_id = u.id
        t.save()
    return redirect('/todo')

def update(request):
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    if request.method == 'POST':
        form = request.form()
        print('debug update', form)
        todo_id = int(form.get('id', -1))
        t = Todo.find_by(id=todo_id)
        t.title = form.get('title', t.title)
        t.save()
    return redirect('/todo')

def delete_todo(request):
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    if t.user_id != u.id:
        return redirect('/login')
    if t is not None:
        t.remove()
    return redirect('/todo')

def delete_todo(request):
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    if t.user_id != u.id:
        return redirect('/login')
    if t is not None:
        t.remove()
    return redirect('/todo')

# 路由字典
# key 是路由(路由就是 path)
# value 是路由处理函数(就是响应)

route_dict = {
    '/todo': index,
    '/todo/edit':edit,
    '/todo/add':login_required(add),
    '/todo/update': update,
    '/todo/delete': delete_todo,
}


