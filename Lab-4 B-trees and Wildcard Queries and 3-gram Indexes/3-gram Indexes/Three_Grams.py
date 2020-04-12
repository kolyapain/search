#
#
#
#

class Three_Grams:
    def __init__(self):
        self.data = dict()

    def update(self, words):
        self.data.clear()
        for word in words:
            w = '$' + word + '$'

            for i in range(len(w) - 2):
                tmp = w[i:(i+3)]
                if tmp in self.data:
                    self.data[tmp].append(word)
                else:
                    self.data[tmp] = [word]
    
    def find(self, request):
        r_list = request.split('*')
        while '' in r_list:
            r_list.remove('')
        
        posible_requests = []
        if len(r_list) == 0:
            posible_requests = ['$']
            request = '*'
        elif len(r_list) == 1:
            if request[0] == '*':
                word = r_list[0] + '$'
            if request[-1] == '*':
                word = '$' + r_list[0]

            if len(word) == 2:
                    posible_requests.append(word)
            else:
                for i in range(len(word) - 2):
                    tmp = word[i:(i+3)]
                    if tmp not in posible_requests:
                        posible_requests.append(tmp)
        else:
            words = ['$' + r_list[0], r_list[-1] + '$']
            for word in words:
                if len(word) == 2:
                    posible_requests.append(word)
                else:
                    for i in range(len(word) - 2):
                        tmp = word[i:(i+3)]
                        if tmp not in posible_requests:
                            posible_requests.append(tmp)

        check_parts = r_list[1:]

        print(posible_requests)
        print(check_parts)
        answers = []
        ids = 0
        for str in posible_requests:
            for key, lst in self.data.items():
                if len(str) == 1:
                    answers.append(lst)
                elif len(str) == 2:
                    if key[1:] == str or key[:-1] == str:    
                        answers.append(lst)
                else:
                    if key == str:    
                        answers.append(lst)

        possible_words = []
        for _answers in answers:
            for ans in _answers:
                ok = True
                if request != '*':
                    if ans[:len(r_list[0])] != r_list[0] and request[0] != '*':
                        continue
                    i = 0
                    for check in check_parts:
                        while check != ans[i:i+len(check)]:
                            i += 1
                            if i >= len(ans):
                                ok = False
                                break
                if ok:
                    if ans not in possible_words:
                        possible_words.append(ans)
        print('p :', possible_words)
        return possible_words