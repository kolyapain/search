#File Parser.py
#Created 02.02.20
#Modified 24.03.20
#Author Semylitko Mykola

from Dictionary import S_Dictionary

class Parser:
    def __init__(self):
        self.symbols = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
            'й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш', 'щ', 'з', 'х', 'ъ', 'ф', 'ы', 'в', 'а', 'п', 'р', 'о', 'л', 'д', 'ж', 'э', 'я', 'ч', 'с', 'м', 'и', 'т', 'ь', 'б', 'ю',
            'Й', 'Ц', 'У', 'К', 'Е', 'Н', 'Г', 'Ш', 'Щ', 'З', 'Х', 'Ъ', 'Ф', 'Ы', 'В', 'А', 'П', 'Р', 'О', 'Л', 'Д', 'Ж', 'Э', 'Я', 'Ч', 'С', 'М', 'И', 'Т', 'Ь', 'Б', 'Ю',
            'Ё', 'ё', 'і', 'І', 'ї', 'Ї', 
            # numbers may not use
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 
            # other symbols
            #'@', '.',
            ]
        self.book_names = []
        self.book_data = []

    def parse_file(self, filename):
        #print(filename)
        enc = self.get_file_encoding(filename)
        has_tags = False
        if enc != 'unknown encoding':
            if filename in self.book_names:
                print("book has already been parsed")
                return None
            if filename[-4:] == 'fb2':
                has_tags = True
            word = ''
            symbol = ''
            f_dict = S_Dictionary()
            with open(filename, encoding=enc) as f:
                while True:
                    try:
                        symbol = f.read(1)
                    except:
                        symbol = ' '

                    if symbol == '<':
                        tag = ''
                        while symbol != '>' and has_tags:
                            try:
                                symbol = f.read(1)
                                tag += symbol
                            except:
                                break
                        continue

                    if not symbol:
                        if len(word) > 1:
                            f_dict.add(word.lower())
                        break

                    if symbol in self.symbols:
                        word += symbol
                    else:
                        if len(word) > 0:
                            f_dict.add(word.lower())
                        word = ''
            return f_dict

    def parse_files(self, filenames_list):
        for filename in filenames_list:
            print("parsing file : ", filename)
            self.parse_file(filename)

    def get_file_encoding(self, filename):
        
        encoding = ['utf-8', 'ANSI']
  
        correct_encoding = ''
  
        for enc in encoding:
            try:
                open(filename, encoding=enc).read()
            except (UnicodeDecodeError, LookupError):
                pass
            else:
                correct_encoding = enc
                return enc
        return 'unknown encoding'


if __name__ == "__main__":
    p = Parser()
    # data = p.parse_file('samples/Fenchenko_berja_L._Arun_Hram_Rassveta.fb2')
    data = p.parse_file('samples/test.fb2')
    print(data.data)