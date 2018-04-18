from jinja2 import Environment, FileSystemLoader
import os.path
from utils import log

# __file__就是本文件的名字
# 得到用于加载模板的目录


path = '{}/templates/'.format(os.path.dirname(__file__))
log('path, ', path)

# 创建一个加载器，jinja2从这个目录中加载模板
loader = FileSystemLoader(path)
# 用加载器创建一个环境，有了它才能读取模板文件
env = Environment(loader=loader)

# 调用get_template方法加载模板并返回
template = env.get_template('demo.html')

#　用render渲染模板
ns = list(range(3))
us = [
    {
        'id': 1,
        'name': 'gua'
    },
    {
        'id': 2,
        'name': '瓜'
    },
]
log(template.render(name='gua',
                    numbers=ns,
                    users=us,
                    foo=1,))