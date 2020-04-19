#File Dictionary.py
#Created 02.02.20
#Author Semylitko Mykola

import csv
import json

class S_Dictionary:
    def __init__(self):
        self.data = list()

    def add(self, word):
        self.data.append(word)

    def clear(self):
        self.data.clear()