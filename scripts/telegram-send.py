import argparse
import json
import requests
import sys


"""Send a message to telegram using a json config file with the following
  info:

  {
    "telegram": {
      "token": bot_token,
      "chat_id": chat_id
    }
  }

  all other elements are ignored
"""


def read_args():
    """Reads the command line arguments and returns the populated namespace"""
    parser = argparse.ArgumentParser(
        description='Send a message to telegram bot')
    parser.add_argument('text', nargs=1, help='text to send')
    parser.add_argument('--config', nargs=1, help='json config file',
                        required=True)
    return parser.parse_args()


def send_msg(text, bot_token, chat_id):
    """Sends the message to the bot"""
    temp = f'http://api.telegram.org/bot{bot_token}/sendMessage?' + \
           f'chat_id={chat_id}&parse_mode=Markdown&text={text}'

    response = requests.get(temp)
    return response.json()


if __name__ == "__main__":
    args = read_args()
    with open(args.config[0], 'r') as config:
        config_data = json.load(config)

    response = send_msg(args.text[0],
                        config_data['telegram']['token'],
                        config_data['telegram']['chat_id'])

    print(json.dumps(response, sort_keys=True, indent=4))
    sys.exit(not response['ok'])
