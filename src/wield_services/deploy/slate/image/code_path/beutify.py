#!/usr/bin/env python

import json
import os
import traceback

from time import sleep

dir_path = os.path.dirname(os.path.realpath(__file__))
print(f"current working dir: {dir_path}")


origin_name = f'{dir_path}/ENERGYGRID'


a = f'{origin_name}.json'

with open(a) as json_file:

    data = json.load(json_file)


    j = json.dumps(data, indent=2, sort_keys=True)

    print(type(j))

    with open(f'{origin_name}_pretty.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)




