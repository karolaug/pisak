'''
Definitions of widgets specific to speller applet
'''
from gi.repository import Mx, GObject
import pisak.widgets


class Button(pisak.widgets.Button):
    __gtype_name__ = "PisakSpellerButton"
    __gproperties__ = {
        "speller_function": (
            GObject.TYPE_STRING,
            "speller function",
            "speller function",
            "noop",
            GObject.PARAM_READWRITE)
    }


class Key(Mx.Button):
    __gtype_name__ = "PisakSpellerKey"
    __gproperties__ = {
        "text": (
            GObject.TYPE_STRING,
            "key text",
            "string appended to a text",
            " ",
            GObject.PARAM_READWRITE),
        "alt_text": (
            GObject.TYPE_STRING,
            "alt key text",
            "AltGr string appended to a text",
            "?",
            GObject.PARAM_READWRITE)
    }


class Text(Mx.Widget):
    __gtype_name__ = "PisakSpellerText"
    

class Prediction(pisak.widgets.Button):
    __gtype_name__ = "PisakSpellerPrediction"
    __gproperties__ = {
        "dictionary": (
            GObject.TYPE_STRING,
            "prediction dictionary",
            "path to source of prediction words",
            "",
            GObject.PARAM_READWRITE)}
