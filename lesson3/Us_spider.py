import requests
import json

url = 'http://music.163.com/#/song?id=551816010'

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'Referer': 'http://music.163.com/#/song?id=551816010',
    'Origin': 'http://music.163.com',
    'Host': 'music.163.com'
}

user_data = {
    'params': 'E/jhd+JvrZ2R5fWqCf8El3dTYVhkeVjEz8OYiWAi8A88v52aHVPHWZsB+VET0ACVR/2D9dFnvJYPDGDjGYxOH/qYefUh+3a1LVMFcpW+/9r7kHGOGsDTj9dVwgAJ2lI55zeSiF1e1PT/90EuJK88DfDoJiLhEzxWuGWLe7BwHFbTqKQNSfTD2CKrX8B20RMk',
    'encSecKey': 'd597e1c2dc9f9a03c638b60f8083181a59a74acd85630672281dff9f5aab58c7eb0ce274e9d76c87ca8d5822ecb23ae1c5adc7245e6db085aa368fb37cc79c462c037369c906a789b7f477a5159777ebbe3178fdf75e037f1e89944af381c567804c8026fea3e1bc0001a8fc1730d5136c223ac17de38f57ae2f5df355beb195'
}

response = requests.get(url, headers=headers, data=user_data)
print(response.text)
data = json.loads(response.text)
hotComments = []
for hotcomment in data['hotComments']:
    item = {
        'nickname': hotcomment['user']['nickname'],
        'content': hotcomment['content'],
        'likedCount': hotcomment['likedCount']
    }
    hotComments.append(hotcomment)

content_list = [content['content'] for content in hotComments]
content_nickname = [content['nickname'] for content in hotComments]
liked_count = [content['likedCount'] for content in hotComments]

print(content_list)