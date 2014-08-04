#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

import pressagio.callback
import pressagio

try:
    import configparser
except ImportError:
    import ConfigParser as configparser


_PATH = os.path.abspath(os.path.split(__file__)[0])


def _local_get(relative):
    return os.path.join(_PATH, relative)


_CONFIG_FILE = _local_get("config.ini")
_CONFIG_PARSER = configparser.ConfigParser()
_CONFIG_PARSER.read(_CONFIG_FILE)


def get_predictions(string):
    callback = CallbackClass(string)
    predictions = pressagio.Pressagio(callback, _CONFIG_PARSER).predict()
    if string[0].isupper():
        predictions = [p[0].upper() + p[1:] for p in predictions]
    if string in predictions:
        predictions.remove(string)
    print(string, predictions)
    return predictions


class CallbackClass(pressagio.callback.Callback):
    def __init__(self, buffer):
        super().__init__()
        self.buffer = buffer

    def past_stream(self):
        return self.buffer
    
    def future_stream(self):
        return ''
