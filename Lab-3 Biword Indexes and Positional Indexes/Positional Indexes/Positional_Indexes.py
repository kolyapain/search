#
#
#
#

from Parser import Parser
import Levenstein_Distance

class Positional_Indexes:
    def __init__(self):
        self.parser = Parser()
        # key -> word, value -> list of dict (key -> book_id, value -> list of word positions)
        self.data = dict()

        # key -> int, value -> book_name
        self.int_to_book = dict()

        # key -> book_name, value -> int
        self.book_to_int = dict()

        self.__unique_id = 0


    def test_parse(self):
        data = self.parser.parse_file('samples/test.txt')
        self.add_book(data, 'samples/test.txt')
        data = self.parser.parse_file('samples/test_2.txt')
        self.add_book(data, 'samples/test_2.txt')

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
        self.add_book(data, book_name)

    def add_book(self, book_data, book_name):
        self.int_to_book[self.__unique_id] = book_name
        self.book_to_int[book_name] = self.__unique_id
        
        for word, positions in book_data.data.items():
            if not word in self.data:
                self.data[word] = dict()
            self.data[word][self.__unique_id] = positions
        
        self.__unique_id += 1
        self.data = dict(sorted(self.data.items()))

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
            for dict_word, sources in self.data.items():
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

    def all_equal(self, lst, ids):
        val = lst[0][ids[0]]
        for i in range(1, len(lst)):
            if lst[i][ids[i]] != val:
                return False
        return True
        
    def step(self, lst, ids):
        min = lst[0][ids[0]]
        min_ids = [0]
        for i in range(1, len(ids)):
            if lst[i][ids[i]] < min:
                min = ids[i]
                min_ids = [i]
            elif lst[i][ids[i]] == min:
                min_ids.append(i)
        
        for id in min_ids:
            if len(lst[id]) == ids[id] + 1:
                return False
            ids[id] += 1
        return True

    def step_first(self, lst, ids):
        if len(lst[0]) == ids[0] + 1:
            return False
        ids[0] += 1

    def step_other(self, lst, ids):
        for i in range(1, len(ids)):
            val = lst[i - 1][ids[i - 1]]
            while lst[i][ids[i]] <= val:
                if len(lst[i]) == ids[i] + 1:
                    return False
                ids[i] += 1
        return True

    def compare_positions(self, words_pos, pos_ids):
        for i in range(1, len(words_pos)):
            if words_pos[i][pos_ids[i]] - words_pos[i - 1][pos_ids[i - 1]] != 1:
                return False
        return True

    def check_positions(self, words_pos, pos_ids):
        while True:
            if self.step_other(words_pos, pos_ids) == False:
                return False
            if self.compare_positions(words_pos, pos_ids) == True:
                return True
            if self.step_first(words_pos, pos_ids) == False:
                return False

    def search(self, _request):
        parsed_request = self.parse_request(_request)
        all_requests = self.find_all_posible_requests(parsed_request)
        if all_requests is None:
            return
        answer = []
        for request in all_requests:
            words_lists = []
            lists_ids = []
            lists = []

            for word in request:
                words_lists.append(self.data[word])
                lists_ids.append(0)
            
            for item in words_lists:
                lists.append(sorted(item.keys()))
            # print(lists)

            local_answer = []

            while True:
                if self.all_equal(lists, lists_ids) == True:
                    id = lists[0][lists_ids[0]]
                    words_pos = []
                    pos_ids = []
                    for item in words_lists:
                        words_pos.append(item[id])
                        pos_ids.append(0)
                    if self.check_positions(words_pos, pos_ids) == True:
                        local_answer.append(id)


                if self.step(lists, lists_ids) == False:
                    break

            for item in local_answer:
                if not item in answer:
                    answer.append(item)
        print("for request", _request)
        print("was analyzed requests", len(all_requests))
        for item in answer:
            print(self.int_to_book[item])

if __name__ == "__main__":
    s = Positional_Indexes()
    s.big_data()
    s.search('too  be  or /2 not  to  be /1')
    