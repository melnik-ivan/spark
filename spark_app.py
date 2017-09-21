import os
import time
import json
from tornado import websocket, web, ioloop

HOST = 'http://192.168.100.7:8888'
users = []
available_user_names = {
    'voluptate', 'deleniti', 'consequuntur', 'itaque', 'asperiores', 'in', 'magni', 'fugiat', 'ut',
    'atque', 'porro', 'molestiae', 'cum', 'quam', 'fuga', 'placeat', 'modi', 'aliquid', 'libero', 'ea',
    'maxime', 'numquam', 'unde', 'voluptatem', 'nobis', 'optio', 'corrupti', 'sed', 'reiciendis',
    'officia', 'consectetur', 'dolorem', 'cupiditate', 'officiis', 'ex', 'accusamus', 'cumque', 'repellat',
    'explicabo', 'enim', 'veniam', 'ipsam', 'rem', 'non', 'doloremque', 'assumenda', 'excepturi', 'quasi',
    'facere', 'odio', 'eos', 'et', 'incidunt', 'nulla', 'maiores', 'voluptatum', 'id', 'blanditiis',
    'quas', 'autem', 'necessitatibus', 'nemo', 'quis', 'voluptas', 'nisi', 'quisquam', 'ratione',
    'eveniet', 'saepe', 'aspernatur', 'beatae', 'delectus', 'dolorum', 'eius', 'qui', 'molestias',
    'ducimus', 'adipisci', 'tenetur', 'commodi', 'accusantium', 'sequi', 'nam', 'error', 'illo', 'quod',
    'doloribus', 'totam', 'harum', 'aut', 'pariatur', 'animi', 'illum', 'sint', 'magnam', 'quos',
    'repellendus', 'labore', 'hic'
}


class Message:
    def __init__(self, sender, raw_message):
        data = json.load(raw_message)
        self.sender = sender
        self.recipient = data['recipient']
        self.time = time.ctime()
        self.content = data['content']

    def to_dict(self):
        return {
            'message': {
                'sender': self.sender,
                'recipient': self.recipient,
                'time': self.time,
                'content': self.content
            }
        }



class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("templates/index.html")


class SocketHandler(websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        websocket.WebSocketHandler.__init__(self, *args, **kwargs)
        self.user_name = None

    def check_origin(self, origin):
        return True

    def open(self):
        pass

    def on_close(self):
        pass

    def on_message(self, data):
        pass


app = web.Application(
    [
        (r'/', IndexHandler),
        (r'/ws', SocketHandler)
    ],
    static_path=os.path.join(os.path.dirname(__file__), "static")
)

if __name__ == '__main__':
    app.listen(8888)
    ioloop.IOLoop.instance().start()
