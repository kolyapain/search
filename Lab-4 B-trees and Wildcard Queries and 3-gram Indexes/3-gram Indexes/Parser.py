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
        if enc != 'unknown encoding':
            if filename in self.book_names:
                print("book has already been parsed")
                return None
            self.book_names.append(filename)

            f_dict = S_Dictionary()
            word = ''
            symbol = ''
            position = 1
            with open(filename) as f:
                while True:
                    try:
                        symbol = f.read(1)
                    except:
                        symbol = ' '

                    if not symbol:
                        if len(word) > 1:
                            f_dict.add(word.lower(), position)
                            position += 1
                        break

                    if symbol in self.symbols:
                        word += symbol
                    else:
                        if len(word) > 0:
                            f_dict.add(word.lower(), position)
                            position += 1
                        word = ''
            return f_dict

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

    def read_samples(self):
        self.parse_files(
            [
                'samples/Dyudeni_Kenterberiyskie_golovolomki_RuLit_Net.txt',
                'samples/Alsina_Mir-matematiki_11_Tom-11-Karty-metro-i-neyronnye-seti-Teoriya-grafov_RuLit_Me.txt',
                'samples/Arbones_Mir-matematiki_12_Tom-12-Chisla-osnova-garmonii-Muzyka-i-matematika_RuLit_Me.txt',
                'samples/Kasalderrey_Mir-matematiki_16_Obman-chuvstv_RuLit_Me.txt',
                'samples/Levshin_Karlikaniya_2_Puteshestvie-po-Karlikanii-i-Al-Dzhebre_RuLit_Me.txt',
                'samples/Levshin_V-labirinte-chisel_RuLit_Net.txt',
                'samples/Loyd_Samyie_znamenityie_golovolomki_mira_RuLit_Net.txt',
                'samples/matematicheskie_chudesa_i_tajjny.u.txt',
                'samples/Navarro_Mir-matematiki_31_Taynaya-zhizn-chisel_RuLit_Me.txt',
                'samples/Smallian_Priklyucheniya_Alisyi_v_Strane_Golovolomok_RuLit_Net.txt',
                'samples/Alone-in-West-Africa-Mary-Gaunt-[ebooksread.com].txt',
                'samples/A-second-solemn-appe-John-Ireland-[ebooksread.com].txt',
                'samples/Catalogue-of-the-Ret-Phyllis-Ackerma-[ebooksread.com].txt',
                'samples/Confidential-Chats-w-William-Lee-How-[ebooksread.com].txt',
                'samples/Famous-Composers-and-Various-[ebooksread.com].txt',
                'samples/Folk-Lore-Notes--Vol-A--M--T--Jackso-[ebooksread.com].txt',
                'samples/On-Sunset-Highways-Thomas-D--Murph-[ebooksread.com].txt',
                'samples/Passages-from-the-Li-Charles-Babbage-[ebooksread.com].txt',
                'samples/Sir-Edwin-Landseer-Frederick-G--St-[ebooksread.com].txt',
                'samples/Studies-in-the-Evolu-Hiram-M---Hiram-[ebooksread.com].txt',
                'samples/Telescopic-Work-for--William-F--Denn-[ebooksread.com].txt',
                'samples/The-Letters-of-a-Por-Marianna-Alcofo-[ebooksread.com].txt',
                'samples/The-Romance-of-a-Sho-Amy-Levy-[ebooksread.com].txt',
            ]
        )

        print("parsed files :")

        for item in self.book_names:
            print(item)