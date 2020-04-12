from Parser import Parser
from Dictionary import S_Dictionary
from collections import OrderedDict

class InvertedIndex(Parser):
    def __init__(self):
        Parser.__init__(self)
        self.word_in_int = dict()
        self.int_for_word = dict()
        self.file_in_int = dict()
        self.int_for_file = dict()
        self.map = dict()

    def read(self):
        self.read_samples()
        self.easy_samples()
        self.init_files_coding()
        self.init_words_coding()
        self.init_inverted_index()

    def init_files_coding(self):
        id = 0
        for file in self.book_names:
            self.file_in_int[file] = id
            self.int_for_file[id] = file
            id += 1

    def init_words_coding(self):
        #sort dict by keys
        id = 0
        sorted_dict = OrderedDict(sorted(self.data.items()))
        for key, _ in sorted_dict.items():
            self.word_in_int[key] = id
            self.int_for_word[id] = key
            id += 1 
        self.data = sorted_dict

    def init_inverted_index(self):
        for key, _ in self.data.items():
            self.map[key] = []


        for i in range(len(self.book_data)):
            s_dict = S_Dictionary()
            s_dict.load_from_json_file(self.book_data[i])

            for key, _ in self.data.items():
                if key in s_dict.data:
                    self.map[key].append(i)                  
                    
        # for key, lst in self.map.items():
        #     print(key, "->", lst)

    def parse_request(self, request):
        all_request = []
        cur_request = []
        for word in request:
            if word == "OR":
                if len(cur_request) > 0:
                    all_request.append(cur_request)
                    cur_request = []
            else:
                cur_request.append(word)

        if len(cur_request) > 0:
            all_request.append(cur_request)

        return all_request


    def parse_loc_request(self, request):
        parsed = []
        not_parsed = []
        not_flag = 0
        for item in request:
            if item == 'AND':
                not_flag = 0
            elif item == 'NOT':
                not_flag = 1- not_flag
            else:
                if not_flag == 0:
                    parsed.append(item)
                else:
                    not_parsed.append(item)
        
        # for item in parsed:
        #     print(item)
        
        # for item in not_parsed:
        #     print("but not ->", item)

        return parsed, not_parsed

    def step_one(self, lists, ids):
        min = lists[0][ids[0]]
        min_ids = [0]
        for i in range(1, len(lists)):
            if lists[i][ids[i]] < min:
                min = lists[i][ids[i]]
                min_ids = [i]
            elif lists[i][ids[i]] == min:
                min_ids.append(i)
        
        for min_id in min_ids:
            ids[min_id] += 1
            if ids[min_id] == len(lists[min_id]):
                return True
        return False

    def step_all(self, lists, ids):
        for i in range(len(lists)):
            ids[i] += 1
            if ids[i] == len(lists[i]):
                return True
        return False

    def all_equal(self, lists, ids):
        value = lists[0][ids[0]]
        for i in range(1, len(lists)):
            if lists[i][ids[i]] != value:
                return -1
        return value

    def boolean_search(self, request):
        # print(self.map)
        answer = []
        not_parsed_request = request
        global_request = self.parse_request(request)
        for req in global_request:
            request, banned = self.parse_loc_request(req)
            # list with answers
            ans = []
            # list with current index for each word in request
            lists = []
            for word in request:
                if word in self.map:
                    lists.append(self.map[word])
                else:
                    print(word, "is unknown")
                    return
            ids = [0] * len(lists)

            ban_list = []
            for word in banned:
                if word in self.map:
                    for item in self.map[word]:
                        if not item in ban_list:
                            ban_list.append(item)    

            # for item in lists:
            #     print(item)
            # print(ids)
            
            if len(lists):
                while True:
                    res = self.all_equal(lists, ids)
                    if res == -1:
                        if self.step_one(lists, ids):
                            break
                    else:
                        ans.append([res, self.int_for_file[res]])
                        if self.step_all(lists, ids):
                            break
            else:
                for i in range(len(self.book_names)):
                    ans.append([i, self.int_for_file[i]])

            for item in ans:
                if not item[0] in ban_list and not item[0] in answer:
                    answer.append(item[1])

        print("on request '", end='')                
        for item in not_parsed_request:
            print(item, end=' ')
        print("' is ", len(answer), "documents :")
        i = 0
        for item in answer:
            print(item)
            i += 1
            if i > 5:
                break


ii = InvertedIndex()
ii.read()
# ii.boolean_search(['text', 'AND', 'file', 'AND', 'NOT', 'fun'])
# ii.boolean_search(['NOT', 'fun', 'AND', 'NOT', 'text'])
ii.boolean_search(['NOT', 'NOT', 'fun', 'AND', 'NOT', 'NOT', 'text', 'OR', 'actually', 'OR', 'NOT', 'is', 'AND', 'NOT', 'my'])
ii.boolean_search([])