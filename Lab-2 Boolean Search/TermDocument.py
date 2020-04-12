from Parser import Parser
from Dictionary import S_Dictionary

class TermDocument(Parser):
    def __init__(self):
        Parser.__init__(self)
        self.word_in_int = dict()
        self.int_for_word = dict()
        self.file_in_int = dict()
        self.int_for_file = dict()
        self.matrix = [] 

    def read(self):
        self.read_samples()
        self.easy_samples()
        self.init_files_coding()
        self.init_words_coding()
        self.build_matrix()

    def init_files_coding(self):
        id = 0
        for file in self.book_names:
            self.file_in_int[file] = id
            self.int_for_file[id] = file
            id += 1

    def init_words_coding(self):
        id = 0
        for key, _ in self.data.items():
            self.word_in_int[key] = id
            self.int_for_word[id] = key
            id += 1

    def build_matrix(self):
        for _ in range(len(self.data)):
            self.matrix.append(list())
        #self.matrix.append([] * len(self.data))

        for file in self.book_data:
            t_dict = S_Dictionary()
            t_dict.load_from_json_file(file)

            for key, _ in self.data.items():
                if key in t_dict.data:
                    self.matrix[self.word_in_int[key]].append(1)
                else:
                    self.matrix[self.word_in_int[key]].append(0)

        # for word, _ in self.data.items():
        #     print(word)
        #     print(self.matrix[self.word_in_int[word]])

    def parse_request(self, words):
        all_request = []
        cur_request = []
        for word in words:
            if word == "OR":
                if len(cur_request) > 0:
                    all_request.append(cur_request)
                    cur_request = []
            else:
                cur_request.append(word)

        if len(cur_request) > 0:
            all_request.append(cur_request)

        return all_request
        

    def boolean_search(self, words):
        all_req = self.parse_request(words)
        answer = []

        for req in all_req:
            print(req)
            not_flag = 0
            mask = [1] * len(self.book_names)

            for word in req:

                if word == "AND":
                    not_flag = 0
                    
                elif word == "NOT":
                    not_flag = 1 - not_flag

                else:
                    word = word.lower()
                    id = self.word_in_int[word]
                    for i in range(len(self.book_names)):
                        if not not_flag:
                            mask[i] &= mask[i] & self.matrix[id][i]
                        else:
                            mask[i] &= mask[i] & (not self.matrix[id][i])

                loc_answer = []
                for i in range(len(mask)):
                    if mask[i] == 1:
                        loc_answer.append(self.int_for_file[i])  
            print(loc_answer)

            for item in loc_answer:
                if not item in answer:
                    answer.append(item)    

        print("on request '", end='')                
        for item in words:
            print(item, end=' ')
        
        print("' is ", len(answer), "documents :")
        i = 0
        for item in answer:
            print(item)
            i += 1
            if i > 5:
                break

t = TermDocument()
t.read()
t.boolean_search(['NOT', 'NOT', 'fun', 'AND', 'NOT', 'NOT', 'text', 'OR', 'actually', 'OR', 'NOT', 'is', 'AND', 'NOT', 'my'])
t.boolean_search([])
# t.boolean_search(['text', 'AND', 'file', 'AND', 'NOT', 'fun'])