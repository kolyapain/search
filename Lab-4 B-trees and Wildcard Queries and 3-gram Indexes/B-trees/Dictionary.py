#File Dictionary.py
#Created 02.02.20
#Author Semylitko Mykola

import csv
import json

class S_Dictionary:
    def __init__(self):
        #print("Dictionary init")
        self.data = dict()

    def print_dict(self):
        if len(self.data) == 0:
            print("Dictionary empty")
        else:
            for key, value in self.data.items():
                print(key, " : ", value)

    def add(self, key):
        if key in self.data:
            old_value = self.data[key]
            self.data[key] = old_value + 1
        else:
            self.data[key] = 1

    def clear(self):
        self.data.clear()

    def save_in_csv_file(self, filename):
        try:
            with open(filename, 'w', encoding='ANSI') as csvfile:
                for key, value in self.data.items():
                    csvfile.write(key + " " + str(value) + "\n")
                    #print(item)
        except IOError:
            print("I/O error")

    def read_from_csv_file(self, filename):
        with open(filename, 'r') as f:
                while True:
                    symbol = f.read(1)
                    key = ''
                    value = ''

                    if not symbol:
                        break

                    while symbol != ' ':
                        key += symbol
                        symbol = f.read(1)

                    symbol = f.read(1)
                    while symbol != '\n':
                        value += symbol
                        symbol = f.read(1)
                    
                    self.data[key] = value

        #self.print()

    def save_in_json_file(self, filename):
        with open(filename, 'w', encoding='ANSI') as fp:
            json.dump(self.data, fp, indent=1, sort_keys=True)

    def load_from_json_file(self, filename):
        with open(filename, 'r', encoding='ANSI') as f:
            self.data = json.load(f)

    def test(self):
        tmp = S_Dictionary()
        tmp.print_dict()
        tmp.add("229")
        tmp.add("what")
        tmp.add("what")
        tmp.print_dict()
        tmp.clear()
        tmp.print_dict()
