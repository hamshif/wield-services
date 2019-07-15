#!/usr/bin/env python
import sys
import json
import requests


def call_service(outside_call=True, protocol='http', domain='localhost',
                 service_name='whisperer', service_port='8002',
                 index='hello', payload=None, headers=None):

    if outside_call:

        url = f'{protocol}://{domain}:{service_port}/{index}'
    else:
        url = f'{protocol}://{service_name}:{service_port}/{index}'

    try:
        g = requests.get(url=url)
        print(f'a is: {g}')

        r = requests.post(f'{url}', data=json.dumps(payload), headers=headers)

        print(f'The text returned from the server: {r.text}')

        return r.text
        # return json.loads(r.content)
    except Exception as e:
        raise Exception(f"Error occurred while trying to call service: {e}")


if __name__ == "__main__":

    args = sys.argv
    l = len(args)

    if l > 1:

        _outside_call = True if args[1] == 'true' else False
    else:
        _outside_call = False

    a = call_service(payload={'key': 'value'}, outside_call=_outside_call)

    print(f'a is: {a}')
