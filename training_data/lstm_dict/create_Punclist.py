
def create_punclist():

    punc1 = ['。', '、', '！', '？', '・']
    punc2 = [
        { 'starting': '（', 'closing' : '）' },
        { 'starting': '「', 'closing' : '」' },
        { 'starting': '『', 'closing' : '』' },
        { 'starting': '［', 'closing' : '］' },
        { 'starting': '〔', 'closing' : '〕' },
        { 'starting': '〈', 'closing' : '〉' },
        { 'starting': '【', 'closing' : '】' }
    ]

    punc3 ='︙'

    li = []
    for i in punc2:
        a = i['starting'] + ' ' + i['closing']
        li.append(a)

        for j in punc1:
            b = j + i['closing']
            li.append(b)
            
            c = i['closing'] + j
            li.append(c)
    
    for k in range(1, 11):
        d = punc3*k
        li.append(d)
    
    punc_list = punc1 + li
    ListTxt = '\n'.join(punc_list)

    with open('./new_jpn_vert.punc', mode='w') as f:
        f.write(ListTxt)

if __name__ == '__main__':
    create_punclist()