#
#
#
#

from Parser import Parser
import Levenstein_Distance
from rank_bm25 import BM25Okapi
from Wildcard_Queries import Wildcard_Queries

class Positional_Indexes:
    def __init__(self):
        self.parser = Parser()
        # key -> word, value -> list of dict (key -> book_id, value -> list of word positions)
        self.data = []
        self.all_words = []

        # key -> int, value -> book_name
        self.int_to_book = dict()

        # key -> book_name, value -> int
        self.book_to_int = dict()

        self.__unique_id = 0

        self.wildcard = Wildcard_Queries()
        self.bm_25 = None

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
                'samples/test.fb2',
            ]

        for book in book_list:
            self.parse_book(book)

        self.wildcard.update(self.all_words)
        self.bm_25 = BM25Okapi(self.data)


    def parse_book(self, book_name):
        data = self.parser.parse_file(book_name)
        self.add_book(data, book_name)

    def add_book(self, book_data, book_name):
        self.int_to_book[self.__unique_id] = book_name
        self.book_to_int[book_name] = self.__unique_id
        
        for word in book_data.data:
            if word not in self.all_words:
                self.all_words.append(word)

        self.data.append(book_data.data)
        
        self.__unique_id += 1

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

    def find_all_posible_requests(self, request):
        all_posible_requests = [[]]
        for word, dist in request:
            w_num = 0
            ok = False
            for dict_word in self.all_words:
                if Levenstein_Distance.calculate(word, dict_word) <= dist:
                    ok = True
                    if w_num == 0:
                        for i in range(len(all_posible_requests)):
                            all_posible_requests[i].append(dict_word)
                    else:
                        if len(all_posible_requests[0]) == 1:
                            all_posible_requests.append([dict_word])
                            continue
                        new_reqs = []
                        for req in all_posible_requests:
                            if req[:-1] not in new_reqs:
                                new_reqs.append(req[:-1])
                        for item in new_reqs:
                            item.append(dict_word)
                            all_posible_requests.append(item)
                    w_num += 1
            if not ok:
                print('no words like : "', word, '" with lev dist = ', dist, sep='')
                return None

        # for req in all_posible_requests:
        #     for word in req:
        #         print(word, end=' ')
        #     print(end='\n')
        return all_posible_requests
      
    def parse_jokers(self, request):
        request_words = request.split()
        all_posible_requests = [[]]
        for word in request_words:
            if '*' in word:
                posible_words = self.wildcard.find(word)
                if len(posible_words) == 0:
                    raise('no words like', word)
                # print('for word', word, 'posible  words', posible_words) 
            else:
                posible_words = [word]

            w_num = 0
            for p_word in posible_words:
                if w_num == 0:
                    for i in range(len(all_posible_requests)):
                        all_posible_requests[i].append(p_word)
                else:
                    if len(all_posible_requests[0]) == 1:
                        all_posible_requests.append([p_word])
                        continue
                    new_reqs = []
                    for req in all_posible_requests:
                        if req[:-1] not in new_reqs:
                            new_reqs.append(req[:-1])
                    for item in new_reqs:
                        item.append(p_word)
                        all_posible_requests.append(item)
                w_num += 1

        # for req in all_posible_requests:
        #     for word in req:
        #         print(word, end=' ')
        #     print(end='\n')
        return all_posible_requests


    def search(self, _request):
        posible_requests = self.parse_jokers(_request)
        for _p_req in posible_requests:
            request_str = ' '.join(item for item in _p_req)
            parsed_request = self.parse_request(request_str)
            all_requests = self.find_all_posible_requests(parsed_request)
            if all_requests is None:
                return

            answer = dict()
            for request in all_requests:
                print("for request '", request_str, "'")
                
                doc_scores = self.bm_25.get_scores(request)

                for i in range(len(doc_scores)):
                    print(i, doc_scores[i])
                    if i not in answer:
                        answer[i] = doc_scores[i]
                    else:
                        if doc_scores[i] > answer[i]:
                            answer[i] = doc_scores[i]

            print("was analyzed requests", len(all_requests))
            for k, v in sorted(answer.items(), key = lambda kv:(-kv[1], kv[0])):
                print(self.int_to_book[k])

if __name__ == "__main__":
    s = Positional_Indexes()
    s.big_data()
    # s.test_parse()
    # print(s.data)
    s.search('to be')
    