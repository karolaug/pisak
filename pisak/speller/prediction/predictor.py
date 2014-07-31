#!/usr/bin/python3
# -*- coding: utf-8 -*-

#this script is used for testing the word prediction feature
#enter words to predict their continuation 
#up to two previous words of context are used in the prediction
#enter an empty string to end the script

import os

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import pressagio.callback
import pressagio


_PATH = os.path.abspath(os.path.split(__file__)[0])


def _local_get(relative):
    return os.path.join(_PATH, relative)


config_file = _local_get("prediction_profile.ini") #set configuration to use
config = configparser.ConfigParser()
config.read(config_file)


def get_predictions(string):
    callback = CallbackClass(string)
    return pressagio.Pressagio(callback, config).predict()


class CallbackClass(pressagio.callback.Callback): #basic callback class
    def __init__(self, buffer):
        super().__init__()
        self.buffer = buffer

    def past_stream(self):
        return self.buffer
    
    def future_stream(self):
        return ''


if __name__ == "__main__":
    print('Enter string: \n')
    while True: #test loop
            string = input()
            if string == '': #ending
                    break
 
            callback = CallbackClass(string)
            prsgio = pressagio.Pressagio(callback, config)
            predictions = prsgio.predict()
            if string[-1] != ' ': # if the string ends with a unfinished word predict it's ending
                    n = len(string.split()[-1]) 
                    string = string[:-n-1] #format the string to display predictions

                    if len(string) != 0:
                            for i in predictions:	
                                    print(string + ' ' + i)

                    else:
                            for i in predictions:	
                                    print(i)

	
            else: #if the string ends with a space predict the next word based on the previous ones
                    for i in predictions:	
                            print(string + i)
            print("\n")
    
