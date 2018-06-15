import os
import logging
import urllib
import random

logger = logging.getLogger()
logger.setLevel(logging.INFO)

BOT_TOKEN = os.environ.get('BOT_TOKEN')
SLACK_URL = "https://slack.com/api/chat.postMessage"

random_sentence = [
    '簡單。真的很簡單'
]


def lambda_handler(data, context):
    try:
        slack_event = data['event']

        if 'command' in slack_event:
            handle_command(slack_event)
        elif "bot_id" not in slack_event:

            text = slack_event.get('text')
            array_text = text.split()
            if array_text[1] == 'random':
                random_word = text.split()[2:]
                text = random.choice(random_word)
            else:
                text = random.choice(random_sentence)

            post_message(text, slack_event["channel"])

    except Exception as e:
        print(e)

    return {
        "text": "已發送"
    }


def post_message(word, channel_id):
    print(word, channel_id)
    data = urllib.parse.urlencode(
        (
            ("token", BOT_TOKEN),
            ("channel", channel_id),
            ("text", word)
        )
    )
    data = data.encode("ascii")

    request = urllib.request.Request(
        SLACK_URL,
        data=data,
        method="POST"
    )

    request.add_header(
        "Content-Type",
        "application/x-www-form-urlencoded"
    )

    urllib.request.urlopen(request).read()


def handle_command(event):
    if event['command'] == '/andy_fuck':
        text = '{}啦幹 :angry_hey:'.format(event.get('text'))
    else:
        text = event.get('text')

    post_message(text, event['channel_id'])
