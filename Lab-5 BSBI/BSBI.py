#
#
#
#

import sys
import json
import os
from Parser import Parser
import mmap

class mmap_record:
    def __init__(self, filename):
        self.filename = filename
        self.file_size = os.path.getsize(filename)
        self.page = 0
        self.offset = 0
        self.buff = ''
        self.ok_flag = True
        self.mmap_readpage()

    def mmap_readpage(self):
        # print('reading next page')
        f = open(self.filename, 'r+')
        r_len = mmap.ALLOCATIONGRANULARITY

        if (self.page + 1) * r_len > self.file_size:
            r_size = self.file_size - self.page * r_len
        else:
            r_size = r_len

        if r_size < 0:
            self.buff = ''
            return False
        try:
            map = mmap.mmap(f.fileno(), length=r_size, offset=r_len * self.page)
            self.buff = map.read(r_size).decode('ansi')
            # print(len(self.buff))
            map.close()
            self.offset = 0
            self.page += 1
            return True
        except Exception as err:
            print(err)
        return False

    def read_next_string(self):
        str = ''
        if self.offset >= len(self.buff):
            return ''
        while self.buff[self.offset] != '\n':
            str += self.buff[self.offset]
            self.offset += 1
            if self.offset >= len(self.buff):
                if self.mmap_readpage() == False:
                    return str
        else:
            self.offset += 1
            if self.offset >= len(self.buff):
                if self.mmap_readpage() == False:
                    return str
        return str

class BSBI:
    def __init__(self):
        self.current_block = 0
        self.block_size = 0
        self.max_block_size = 16384 * 64
        self.parser = Parser()
        self.block = list()

    def invert_block(self):
        self.current_block += 1
        with open('blocks/block_'+str(self.current_block)+'.txt', 'w') as fp:
            for word, file, positions in sorted(self.block):
                    fp.write(word + ' ' + file)
                    for pos in positions:
                        fp.write(' ' + str(pos))
                    fp.write('\n')
        self.block.clear()

    def parse_file(self, filename):
        data = self.parser.parse_file(filename).data
        fname_size = len(filename)
        for word, positions in data.items():
            pos_len = 0
            for pos in positions:
                pos_len += len(str(pos)) + 2
            record_size = len(word) + fname_size + pos_len
            if  record_size + self.block_size > self.max_block_size:
                # print(record_size, self.block_size, self.max_block_size)
                self.block_size = 0
                self.invert_block()
            
            self.block.append([word, filename, positions])
            self.block_size += record_size

    def step_min(self, words):
        if len(words) == 0:
            return None
        
        min = words[0][0]
        ids = [0]
        for i in range(1, len(words)):
            if words[i][0] < min:
                min = words[i][0]
                ids = [i]
            elif words[i][0] == min:
                ids.append(i)
        
        return ids

    def find_min_word(self, words):
        if len(words) == 0:
            return None

        min = words[0][0]
        for i in range(1, len(words)):
            if words[i][0] < min:
                min = words[i][0]
        return min

    def merge_blocks(self):
        maps = []
        ### initial mmap for all blocks
        # for i in range(self.current_block):
        for i in range(10):
            maps.append(mmap_record('blocks/block_'+str(i + 1)+'.txt'))

        ws_pairs = [[]] * len(maps)

        for i in range(len(maps)):
            line = maps[i].read_next_string()
            word, source = line[:-1].split(' ', 1)
            ws_pairs[i] = [word, source]
        # print(ws_pairs)
        f_index = open('index.txt', 'w')
        sources = []
        prev_min_word = self.find_min_word(ws_pairs)
        while len(maps) > 0:
            min_word = self.find_min_word(ws_pairs)

            # if min_word is new word then we get all sources for prev min word
            if min_word != prev_min_word:
                f_index.write(prev_min_word + ' ' + str(len(sources)))
                for source in sources:
                    f_index.write(' ' + source + ';')
                f_index.write('\n')
                sources = []

            # save all sources for min word on current iteration
            for w, s in ws_pairs:
                if w == min_word:
                    sources.append(s)

            # save current word to prev
            prev_min_word = min_word

            next_min_ids = self.step_min(ws_pairs)
            if next_min_ids is None:
                break

            # read next words for min ids
            ids_to_pop = []
            for i in next_min_ids:
                line = maps[i].read_next_string()
                if line != '':
                    word, source = line[:-1].split(' ', 1)
                    ws_pairs[i] = [word, source]
                else:
                    ids_to_pop.append(i)
            ids_del = 0
            for i in ids_to_pop:
                maps.pop(i - ids_del)
                ws_pairs.pop(i - ids_del)
                ids_del += 1
            
        # save not save word
        if prev_min_word:    
            f_index.write(prev_min_word + ' ' + str(len(sources)))
            for source in sources:
                f_index.write(' ' + source)
            f_index.write('\n')

        f_index.close()


    def bsbi(self, files):
        for file in files:
            self.parse_file(file)
        if len(self.block) > 0:
            self.invert_block()

        self.merge_blocks()

if __name__ == "__main__":
    b = BSBI()
    # b.bsbi([
    #     'samples/test.txt', 
    #     'samples/test_2.txt',
    #     'samples/Alsina_Mir-matematiki_11_Tom-11-Karty-metro-i-neyronnye-seti-Teoriya-grafov_RuLit_Me.txt',
    #     'samples/Arbones_Mir-matematiki_12_Tom-12-Chisla-osnova-garmonii-Muzyka-i-matematika_RuLit_Me.txt',
    #     'samples/Kasalderrey_Mir-matematiki_16_Obman-chuvstv_RuLit_Me.txt',
    #     'samples/Levshin_Karlikaniya_2_Puteshestvie-po-Karlikanii-i-Al-Dzhebre_RuLit_Me.txt',
    #     'samples/Levshin_V-labirinte-chisel_RuLit_Net.txt',
    #     'samples/Loyd_Samyie_znamenityie_golovolomki_mira_RuLit_Net.txt',
    #     'samples/matematicheskie_chudesa_i_tajjny.u.txt',
    #     'samples/Navarro_Mir-matematiki_31_Taynaya-zhizn-chisel_RuLit_Me.txt',
    #     'samples/Smallian_Priklyucheniya_Alisyi_v_Strane_Golovolomok_RuLit_Net.txt',
    #     'samples/Sir-Edwin-Landseer-Frederick-G--St-[ebooksread.com].txt',
    #     'samples/The-Letters-of-a-Por-Marianna-Alcofo-[ebooksread.com].txt',
    #     'samples/The-Romance-of-a-Sho-Amy-Levy-[ebooksread.com].txt',
    # ])
    b.bsbi([])