#File Dictionary.py
#Created 02.02.20
#Author Semylitko Mykola

import csv
import json

class S_Dictionary:
    def __init__(self):
        self.data = dict()

    def add(self, word, pos):
        if word in self.data:
            self.data[word].append(pos)
        else:
            self.data[word] = [pos]

    def clear(self):
        self.data.clear()