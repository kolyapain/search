#File Parser.py
#Created 02.02.20
#Author Semylitko Mykola

from Dictionary import S_Dictionary

class Parser(S_Dictionary):
    def __init__(self):
        S_Dictionary.__init__(self)

        # Bad idea
        # self.delimiters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '-',
        #               '{', '}', '[', ']', ':', ';', '"', "'", '<', '>', '?', '/', '|', "\\", 
        #               ' ', '\n', '\t', '\0', ',', '«', '»', '–', '.', '=', '—', '›', '’',
        #               '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '␜', '‘', '‘', '“', '”', '”'
        #               '\x98', '\xE2', '\x90', '\xBC', '\xa0', '\x91', '\x92', '\x93', '\x94'
        #               ]
                      
        # Better one              
        self.symbols = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
            'й', 'ц', 'у', 'к', 'е', 'н', 'г', 'ш', 'щ', 'з', 'х', 'ъ', 'ф', 'ы', 'в', 'а', 'п', 'р', 'о', 'л', 'д', 'ж', 'э', 'я', 'ч', 'с', 'м', 'и', 'т', 'ь', 'б', 'ю',
            'Й', 'Ц', 'У', 'К', 'Е', 'Н', 'Г', 'Ш', 'Щ', 'З', 'Х', 'Ъ', 'Ф', 'Ы', 'В', 'А', 'П', 'Р', 'О', 'Л', 'Д', 'Ж', 'Э', 'Я', 'Ч', 'С', 'М', 'И', 'Т', 'Ь', 'Б', 'Ю',
            'Ё', 'ё', 'і', 'І', 'ї', 'Ї', 
            # numbers may not use
            #'1', '2', '3', '4', '5', '6', '7', '8', '9', '0' 
            ]

        self.book_names = []
        self.book_data = []
        print("Parser init")

    def parse_file(self, filename):
        #print(filename)
        enc = self.get_file_encoding(filename)
        if enc != 'unknown encoding':
            f_dict = S_Dictionary()
            word = ''
            symbol = ''
            if filename in self.book_names:
                print("book has already been parsed")
                return
            self.book_names.append(filename)
            with open(filename) as f:
                while True:

                    try:
                        symbol = f.read(1)
                    except:
                        symbol = ' '

                    if not symbol:
                        if len(word) > 1:
                            f_dict.add(word.lower())
                            self.add(word.lower())
                        break

                    if symbol in self.symbols:
                        word += symbol
                    else:
                        if len(word) > 0:
                            f_dict.add(word.lower())
                            self.add(word.lower())
                        word = ''

            json_name = "./data/" + filename[8:-3] + "json"
            print("saving in ", json_name ,"\n")
            self.book_data.append(json_name)
            f_dict.save_in_json_file(json_name)

            # csv_name = "./data/" + filename[8:-3] + "csv"
            # print("saving in ", csv_name ,"\n")
            # self.book_data.append(csv_name)
            # f_dict.save_in_csv_file(csv_name)
            

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
                print(correct_encoding)
                return enc
        return 'unknown encoding'

    def easy_samples(self):
        self.parse_files(
            [
                'samples/easy_1.txt',
                'samples/easy_2.txt',
                'samples/easy_3.txt',
                'samples/doc_1.txt',
                'samples/doc_2.txt',
            ])

        self.save_in_csv_file("all_data.csv")
        self.save_in_json_file("all_data.json")

        print("parsed files :")

        for item in self.book_names:
            print(item)

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

        self.save_in_csv_file("all_data.csv")
        self.save_in_json_file("all_data.json")

        print("parsed files :")

        for item in self.book_names:
            print(item)

# p = Parser()
# p.read_samples()
# p.clear()
#p.read_from_csv_file("./data/Alone-in-West-Africa-Mary-Gaunt-[ebooksread.com].csv")
# p.load_from_json_file("all_data.json")
#p.print()