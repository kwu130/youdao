import requests
import json
import sys
from time import sleep
from urllib.parse import quote

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

API = "YouDaoCV"
API_KEY = "659600698"

def print_result(data):
    #has_result = False
    if 'basic' in data:
        has_result = True
        _basic = data['basic']
        if 'uk-phonetic' in _basic and 'us-phonetic' in _basic:
            print(" [Word Pronunciation]")
            print(" * UK: [{}]" .format(_basic['uk-phonetic']), end = ',')
            print(" US: [{}]" .format(_basic['us-phonetic']))
        elif 'phonetic' in _basic:
            print(" [Word Pronunciation]")
            print(" [{}]" .format(_basic['phonetic']))
        else:
            pass
        if 'explains' in _basic:
            print("\n [Word Explanation]")
            print(*map(" * {0}".format, _basic['explains']), sep = '\n')
        else:
            print()
    elif 'translation' in data:
        has_result = True
        print(" [Translation]")
        print(*map(" * {0}".format, data['translation']), sep = '\n')
    else:
        pass
    
    if 'web' in data:
        has_result = True
        _web = data['web']
        print("\n [Web Reference]")
        for i in range(len(_web)):
            value = _web[i]['value']
            key = _web[i]['key']
            print(" *", end = '')
            print(*map(" {0}".format, value), sep = ',', end = ': ')
            print(key)
    else:
        pass
    print()
    if not has_result:
        print("No result for this query!")


def translate_word(WORD):
    try:
        url = "http://fanyi.youdao.com/openapi.do?keyfrom={0}&key={1}&type=data&doctype=json&version=1.1&q={2}".format(API, API_KEY, WORD)
        result = requests.get(url, headers = headers)
        if result.status_code != 200:
            raise Exception("Network is unaviliable!")
        else:   
            js = json.loads(result.text)
            print_result(js)
            sleep(0.1)
    except:
        print("Please check your network connection and try agin later!")


def input_word():
    while True:
        word = input("> ").strip()
        word = quote(word)
        if len(word) == 0:
            continue
        elif word == "%5Cq" or word == "%3Aq":
            sys.exit()
        else:
            translate_word(word)

def main():
    input_word()

if __name__ == "__main__":
    main()
