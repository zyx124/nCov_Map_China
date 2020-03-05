import requests
import re
import json
import functools

# This url is provided by Issac Lin on Github
URL = "https://lab.isaaclin.cn/nCoV/api/area"


def get_province_data():
    res = requests.get(URL)
    raw = jsonify(res)

    data = [(p['provinceEnglishName'], p['confirmedCount']) for p in raw if p['countryEnglishName'] == 'China']
    return data

def jsonify(data):
    json_data = json.loads(data.text)

    return json_data['results']
