#!/usr/bin/env python3

import argparse
import dbm
import json
import os
import urllib.request
import urllib.parse
import sys


# Put your API_KEY here
API_KEY = ""
API_ENDPOINT = "https://translate.yandex.net/api/v1.5/tr.json/translate?{}"
DB_FILE = os.path.join(os.environ["HOME"] + "/.yandex_trans.db")


def update_dictdb(lookup_word, response):
    response = json.loads(response.decode("utf-8"))
    meaning = ",".join(response["text"])
    if not dbm.whichdb(DB_FILE):
        with dbm.open(DB_FILE, "n") as dict_db:
            dict_db[lookup_word] = meaning
    else:
        with dbm.open(DB_FILE, "w") as dict_db:
            dict_db[lookup_word] = meaning


def lookup(word):

    with dbm.open(DB_FILE, "w") as dict_db:
        if word in dict_db:
            return dict_db[word].decode("utf-8")

    params = urllib.parse.urlencode({"lang": "en-th", "key": API_KEY})
    url = API_ENDPOINT.format(params)
    data = urllib.parse.urlencode({"text": word}).encode("utf8")

    r = urllib.request.urlopen(url, data)
    response = r.read()
    update_dictdb(word, response)

    return lookup(word)
    # return response.decode("utf-8")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="text to translate")
    parser.add_argument("text", type=str, help="text to translate to Thai")
    args = parser.parse_args()

    translated = lookup(args.text)
    print("{} | {}".format(args.text, translated))
