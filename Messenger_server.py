from flask import request, abort, Flask
import time

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, it is "Sashko" local server'


@app.route('/status')
def stat():
    return {
        'Name': 'Sashko',
        'Status': True,
        'Time': time.time()

    }


messages = []


@app.route('/send', methods=['POST'])
def send_message():

    #Створюємо метод для відправки повідомлення на сервер

    data = request.json
    if not isinstance(data, dict):
        return abort(400)

    name = data.get('name')
    text = data.get('text')

    #Перевіряємо наші данні

    if 'name' not in data or not isinstance(name, str):
        return abort(400)

    if 'text' not in data or not isinstance(text, str) or \
            len('text') == 0 or len('text') > 1000:
        return abort(400)

    message = {
        'name': name,
        'text': text,
        'time': time.time()
    }

    messages.append(message)
    return {'ok': True}


@app.route('/messages')
def get_messages():
    #Створюємо метод для отримання повідомлень
    try:
        after = float(request.args['after'])

    except:
        return abort(400)

    response = []
    for message in messages:
        if message['time'] > after:
            response.append(message)
    return {'messages': response[:50]}


app.run()
