import os
import time
import json
from tornado import websocket, web, ioloop

HOST = 'http://192.168.100.7:8888'
users = []
errors = {
    'username_error': {
        'error': 'username_error',
        'note': ''
    },
    'recipient_error': {
        'error': 'recipient_error',
        'note': ''
    }
}
notice = {
    'connect_user': {
        'user': {
            'connect': 'user_name'
        }
    },
    'disconnect_user': {
        'user': {
            'disconnect': 'user_name'
        }
    }
}
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
        self.sender = sender
        self.recipient = raw_message['recipient']
        self.time = time.ctime()
        self.content = raw_message['content']

    def set_sender(self, user_name):
        self.sender = user_name

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

    def release_user_name(self):
        available_user_names.add(self.user_name)
        self.user_name = None

    def set_username(self, user_name=''):
        if len(available_user_names) > 0:
            self.user_name = available_user_names.pop()
            return self.user_name
        else:
            return False

    def error_handler(self, error_type, note=''):
        error = errors[error_type]
        if note:
            error['note'] = note
        return error

    def notify_connect_user(self):
        notification = notice['connect_user']
        notification['user']['connect'] = self.user_name
        for user in users:
            user.write_message(notification)

    def notify_disconnect_user(self):
        notification = notice['disconnect_user']
        notification['user']['disconnect'] = self.user_name
        for user in users:
            user.write_message(notification)

    def get_user_by_name(self, user_name):
        for user in users:
            if user_name == user.user_name:
                return user
        return False

    def send_message(self, data):
        message = Message(self.user_name, data)
        if message.recipient == self.user_name:
            self.write_message(message.to_dict())
            message.set_sender('echo')
            self.write_message(message.to_dict())
        else:
            message_dict = message.to_dict()
            self.write_message(message_dict)
            recipient = self.get_user_by_name(message.recipient)
            if recipient:
                recipient.write_message(message_dict)
            else:
                self.write_message(self.error_handler('recipient_error', 'user is offline'))

    def check_origin(self, origin):
        return True

    def open(self):
        self.set_username()
        if self.user_name:
            users.append(self)
            self.write_message({'user_name': self.user_name})
        else:
            self.write_message(self.error_handler('username_error', 'user name not available'))

    def on_close(self):
        self.release_user_name()
        users.remove(self)
        self.notify_disconnect_user()

    def on_message(self, data):
        data = json.loads(data)
        if 'message' in data.keys():
            self.send_message(data['message'])


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
