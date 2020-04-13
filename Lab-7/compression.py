class ByteCodec:
    @staticmethod
    def encode(number):
        s_num = '1' + "{0:b}".format(number)

        if len(s_num) == 8:
            return s_num
        
        if len(s_num) < 8:
            zstr = '0' * (8 - len(s_num))
            s_num = '1' + zstr + s_num[1:]
            return s_num

        s_num = s_num[1:]

        i = len(s_num) - 7
        s_num = s_num[:i] + '1' + s_num[i:]
        i -= 7
        while i > 0:
            s_num = s_num[:i] + '0' + s_num[i:]
            i -= 8

        nlen = 8 * (len(s_num) // 8 + 1) - len(s_num)
        zstr = '0' * nlen
        s_num = zstr + s_num

        return s_num

    @staticmethod
    def decode(bit_str):
        if len(bit_str) > 8:
            s = bit_str[:8]
            i = 8
            while i < len(bit_str):
                s += bit_str[i+1:i+8]
                i += 8
        else:
            s = bit_str[1:]

        v = int(s, 2)
        return v
        
    @staticmethod
    def parse_bit_str(bit_str):
        if len(bit_str) % 8 != 0:
            print('bad str')
            return None
        
        values = []
        i = 0
        s = ''
        size_s = len(bit_str) // 8
        while i < size_s:
            tmp = bit_str[8*i:8*(i+1)]
            s += tmp
            if tmp[0] == '1':
                print(s)
                n = ByteCodec.decode(s)
                values.append(n)
                s = ''
            i += 1
        return values
            
class Dict_Compression:
    def __init__(self):
        self.big_string = ''
        self.table = []

    def add_word(self, word):
        lenght = len(self.big_string)
        self.table.append(lenght)
        self.big_string += word

    def get_word(self, id):
        if id == len(self.table):
            return None
        if id + 1 != len(self.table):
            return self.big_string[self.table[id]:self.table[id + 1]]
        return self.big_string[self.table[id]:]

    def find_word(self, word):
        l = 0
        r = len(self.table) - 1

        while l <= r:
            id = (l + r) // 2
            res = self.get_word(id)
            if res == word:
                return id
            if word < res:
                r = id - 1
            else:
                l = id + 1
        return None

if __name__ == "__main__":
    while True:
        try:
            num = int(input())
        except:
            break
        s = ByteCodec.encode(num)
        l = len(s) // 8
        print(len(s))
        for i in range(l):
            print(s[8*i:8*(i+1)]) 
        print(hex(int(s, 2))[2:])

        print('decoded', ByteCodec.decode(s))
    # print(ByteCodec.parse_bit_str('000001101011100010000101000011010000110010110001'))