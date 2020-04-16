#
#
#
#

import Levenstein_Distance
from Wildcard_Queries import Wildcard_Queries
from BSBI import BSBI
from compression import (Dict_Compression, ByteCodec)

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


    def search(self, _request):
        posible_requests = self.parse_jokers(_request)
        for _p_req in posible_requests:
            request_str = ' '.join(item for item in _p_req)
            parsed_request = self.parse_request(request_str)
            all_requests = self.find_all_posible_requests(parsed_request)
            if all_requests is None:
                return
            answer = []
            for request in all_requests:
                print("for request '", request_str, "'")
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
            
            print("was analyzed requests", len(all_requests))
            for item in answer:
                print(self.int_to_book[item])
            print()

if __name__ == "__main__":
    s = Positional_Indexes()
    s.big_data()
    s.search('to /1 be*')
    # while True:
    #     word = input('word to search: ')
    #     if len(word) == 0:
    #         break
        
    #     res = s.compressed_all_words.find_word(word)
    #     if res is None:
    #         print('word : "', word, '" not found')
    #     else:
    #         print('word : "', word, '" found at id : ', res)

