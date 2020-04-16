#
#
#
#

from Parser import Parser
import Levenstein_Distance

class Biword_Indexes:
    def __init__(self):
        self.parser = Parser()
        # key -> book_name, value -> list of biwords
        self.data = dict()

    def test_parse(self):
        self.data['samples/test.txt'] =  self.parser.parse_file('samples/test.txt')
        self.data['samples/test_2.txt'] =  self.parser.parse_file('samples/test_2.txt')

    def big_data(self):
        book_list = [
                'samples/Alsina_Mir-matematiki_11_Tom-11-Karty-metro-i-neyronnye-seti-Teoriya-grafov_RuLit_Me.txt',
                'samples/Arbones_Mir-matematiki_12_Tom-12-Chisla-osnova-garmonii-Muzyka-i-matematika_RuLit_Me.txt',
                'samples/Kasalderrey_Mir-matematiki_16_Obman-chuvstv_RuLit_Me.txt',
                'samples/Levshin_Karlikaniya_2_Puteshestvie-po-Karlikanii-i-Al-Dzhebre_RuLit_Me.txt',
                'samples/Levshin_V-labirinte-chisel_RuLit_Net.txt',
                'samples/Loyd_Samyie_znamenityie_golovolomki_mira_RuLit_Net.txt',
                'samples/matematicheskie_chudesa_i_tajjny.u.txt',
                'samples/Navarro_Mir-matematiki_31_Taynaya-zhizn-chisel_RuLit_Me.txt',
                'samples/Smallian_Priklyucheniya_Alisyi_v_Strane_Golovolomok_RuLit_Net.txt',
                'samples/Sir-Edwin-Landseer-Frederick-G--St-[ebooksread.com].txt',
                'samples/The-Letters-of-a-Por-Marianna-Alcofo-[ebooksread.com].txt',
                'samples/The-Romance-of-a-Sho-Amy-Levy-[ebooksread.com].txt',
                'samples/test_2.txt',
                'samples/test.txt',
        ]

        for book in book_list:
            self.parse_book(book)

    def parse_book(self, book_name):
        data = self.parser.parse_file(book_name)
        if data is None:
            print(book_name)
        else:
            self.data[book_name] = data
        
    def parse_request(self, request):
        request = request.split()
        parsed = []
        for i in range(len(request) - 1):
            if request[i][0] == '/': continue
            if request[i + 1][0] == '/':
                dist = int(request[i + 1][1:])
                parsed.append([request[i], dist])
            else:
                parsed.append([request[i], 0])
        if request[-1][0] != '/':
            parsed.append([request[-1], 0])
        return parsed

    def search(self, _request):
        parsed_request = self.parse_request(_request)
        answer = []

        for book_name, biwords in self.data.items():
            i = 0
            for word1, word2 in biwords:
                if (Levenstein_Distance.calculate(word1, parsed_request[i][0]) <= parsed_request[i][1] and 
                    Levenstein_Distance.calculate(word2, parsed_request[i + 1][0]) <= parsed_request[i + 1][1]):
                    i += 1
                    if i == len(parsed_request) - 1:
                        answer.append(book_name)
                        break
                else:
                    i = 0

        print("for request", _request)
        for item in answer:
            print(item)

if __name__ == "__main__":
    s = Biword_Indexes()
    s.big_data()
    s.search('too  be  or /2 not  to  be /1')
    