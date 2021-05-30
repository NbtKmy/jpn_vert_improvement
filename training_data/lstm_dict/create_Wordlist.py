


def create_wordlist():
    with open('./jpn_vert.wordlist') as f:
        wl = f.readlines()

        

        with open('../titleList.txt') as f:
            tl = f.readlines()

            kanji_num = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '〇']
            al = wl + tl + kanji_num
            newWl = list(set(al))

            '''
            origL = []
            for i in newWl:
                i.strip()
                origL.append(i)
            '''
            ListTxt = ''.join(newWl)

            with open('./new_jpn_vert.wordlist', mode='w') as f:
                f.write(ListTxt)


if __name__ == '__main__':
    create_wordlist()
    
