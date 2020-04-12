#
#
#
#

from suffix_trees import STree

class STree_wrapper:
    def __init__(self, words, reversed_words):
        self.words = STree.STree(words)
        self.rword = STree.STree(reversed_words)

    def contains(self, request):
        straight_words = []
        reversed_words = []

        substrings = request.split('*')
        if '' in substrings:
            substrings.remove('')
        print(substrings)
        for i in range(len(substrings)):
            straight_words.append(substrings[i])
            if len(substrings) > i + 1:
                reversed_words.append(''.join(reversed(substrings[i + 1])))

        print(straight_words)
        print(reversed_words)


        for str in straight_words:
            print(self.words.find_all(str))

        print(self.words.lcs())




if __name__ == "__main__":
    words = [ 'test', 'monday', 'sunday', 'word', 'song', 'qwe', 'asdzxc', 'absdxc' ]
    rwords = []
    for word in words:
        rwords.append(''.join(reversed(word)))
    print(words)
    print(rwords)
    t = STree_wrapper(words, rwords)
    t.contains('qw*as*zx')
