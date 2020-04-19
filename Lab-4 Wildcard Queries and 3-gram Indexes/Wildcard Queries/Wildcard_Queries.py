#
#
#
#

class Wildcard_Queries:
    def __init__(self):
        self.data = []

    def update(self, words):
        self.data.clear()
        for word in words:
            word += '$'
            self.data.append(word)
            while word[0] != '$':
                word = word[1:] + word[0]
                self.data.append(word)
    
    def find(self, request):
        r_list = request.split('*')
        while '' in r_list:
            r_list.remove('')
        possible_words = []
        check_parts = []
        if len(r_list) == 0:
            s_word = '*'
        elif len(r_list) == 1:
            if request[0] == '*':
                s_word = '*' + r_list[0]
            else:
                s_word = r_list[0] + '*'
        else:
            s_word = r_list[0] + '*' + r_list[-1]
            check_parts = r_list[1:-1]
        s_word += '$'
        while s_word[-1] != '*':
            s_word = s_word[-1] + s_word[0:-1]    
        if request[0] == '*':
            str = s_word[s_word.index('$') + 1 : s_word.index('*')]
            s_word = s_word.replace('$' + str + '*', '$*')
            check_parts.insert(0, str)

        s_word_len = len(s_word)
        answers = []
        print(s_word)
        for wildcard in self.data:
            try:
                if s_word[:-1] == wildcard[-s_word_len:] or s_word[:-1] == wildcard[-s_word_len:-1]:
                # if s_word[:-2] in wildcard:
                    tmp = wildcard
                    while tmp[-1] != '$':
                        tmp = tmp[-1] + tmp[:-1]
                    
                    if tmp not in answers:
                        answers.append(tmp)
            except:
                pass

        for ans in answers:
            i = 0
            ok = True
            for check in check_parts:
                while check != ans[i:i+len(check)]:
                    i += 1
                    if i >= len(ans):
                        ok = False
                        break
            if ok:
                possible_words.append(ans[:-1])
        print(possible_words)
        return possible_words