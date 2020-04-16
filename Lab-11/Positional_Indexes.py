#
#
#
#

import Levenstein_Distance
from Wildcard_Queries import Wildcard_Queries
from BSBI import BSBI
from compression import (Dict_Compression, ByteCodec)
import math

class Positional_Indexes:
    def __init__(self):
        # key -> word, value -> list of dict (key -> book_id, value -> list of word positions)
        self.data = dict()
        self.compressed_all_words = Dict_Compression() 
        self.all_words = []

        # key -> int, value -> book_name
        self.int_to_book = dict()

        # key -> book_name, value -> int
        self.book_to_int = dict()

        self.__unique_id = 0

        self.wildcard = Wildcard_Queries()

    def create_index(self):
        pass

    def big_data(self):
        with open('coded_sources.txt') as f:
            lines = f.readlines()
            for l in lines:
                name, code = l.split(' ')
                code = int(code)
                self.book_to_int[name] = code
                self.int_to_book[code] = name
                self.__unique_id = code + 1

        with open('compressed_index.txt', 'r') as f:

            while True:
                line = f.readline()
                if not line:
                    break
        
                word, count, sources = line.split(' ', 2)
                self.all_words.append(word)
                self.compressed_all_words.add_word(word)
                
                books = sources.split(';')
                d = dict()
                prev = 0
                for book in books:
                    if book == '\n':
                        continue
                    if book[0] == ' ':
                        book = book[1:]
                    name, positions = book.split(' ', 1)
                    code_name = ByteCodec.decode(name)
                    code_name = code_name + prev
                    
                    pos = []
                    for i in positions.split(' '):
                        pos.append(int(i))

                    d[code_name] = pos

                self.data[word] = d

        self.wildcard.update(self.all_words)

    def add_book(self, book_data, book_name):
        self.int_to_book[self.__unique_id] = book_name
        self.book_to_int[book_name] = self.__unique_id
        
        for word, positions in book_data.data.items():
            if word not in self.all_words:
                self.all_words.append(word)
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
            if len(lst[id]) <= ids[id] + 1:
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

    def calc_idft(self, term):
        N = len(self.book_to_int)
        dft = len(self.data[term].keys())
        v = N/dft
        v = math.log(v, 2)
        return v

    def scoring(self, request, docs):
        scored = dict()
        for item in docs:
            scored[item] = 0

        for word in request:
            idft = self.calc_idft(word)
            for item in docs:
                tf = len(self.data[word][item])
                scored[item] += idft * tf
        return scored

    def clustering(self, request):
        cluster = dict()

        for word in request:
            tmp = dict()
            cluster[word] = dict()

            for book, _ in self.data[word].items():
                tmp[book] = 0
            idft = self.calc_idft(word)
            for book, _ in self.data[word].items():
                tf = len(self.data[word][book])
                tmp[book] += idft * tf

            tmp = sorted(tmp.items(), key = lambda kv:(-kv[1], kv[0]))
            s = len(tmp) // 2 + 1
            for book, v in tmp[:s]:
                cluster[word][book] = self.data[word][book]
        return cluster

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

                local_answer = self.clustering(request)
                if len(cluster) == 0:
                    break
                # print(cluster)

                
                
                if len(local_answer) > 0:
                    scored = self.scoring(request, local_answer)

                    for k, v in scored.items():
                        if not k in answer:
                            answer[k] = v
                        else:
                            if answer[k] < v:
                                answer[k] = v
            
            print("was analyzed requests", len(all_requests))
            results = sorted(answer.items(), key = lambda kv:(kv[1], kv[0]))
            results.reverse()
            for k, v in results:
                print(k, self.int_to_book[k], 'score :', v)
            print()

if __name__ == "__main__":
    s = Positional_Indexes()
    s.big_data()
    # print(s.data)
    s.search('to /1 be')
    # while True:
    #     word = input('word to search: ')
    #     if len(word) == 0:
    #         break
        
    #     res = s.compressed_all_words.find_word(word)
    #     if res is None:
    #         print('word : "', word, '" not found')
    #     else:
    #         print('word : "', word, '" found at id : ', res)

