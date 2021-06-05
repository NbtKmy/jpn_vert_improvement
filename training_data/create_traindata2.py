import random
import textwrap
from PIL import Image, ImageDraw, ImageFont

def create_train_txt():
    with open('.../wiki_v3.txt') as f:
        txt = f.readlines()
        wiki = random.sample(txt, 1000)

        with open('./titleList.txt') as g:
            titles = g.readlines()
            
            list = []
            for i in wiki:
                i = i.strip()
                list.append(i)
                title = random.choice(titles)
                title = title.strip()
                list.append(title)
            
            new_text = ''.join(list)
            # Einige Schriftzeichen wie "(" (Halbbreite-Klammer) ersetzen
            new_text = new_text.replace(' ', '')
            new_text = new_text.replace('(', '（')
            new_text = new_text.replace(')', '）')

            while len(new_text) < 30000:
                add_txt = random.choice(wiki)
                new_text = new_text + add_txt

            new_text = textwrap.wrap(new_text, width=30)

            # Simulation der Seitenzahl
            kanji_num = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '〇']
            dgt_list = [1, 2, 3]
            jpn_nums = []
            for l in range(1000):
                dgt = random.choice(dgt_list)
                n = ''.join(random.choices(kanji_num, k=dgt))
                jpn_nums.append(n)
            
            traintxt_list = []
            for m in range(1000):
                d = len(jpn_nums[m])
                t = new_text[m] + '︙'*(10-d) + jpn_nums[m]
                traintxt_list.append(t)

            traintxt = '\n'.join(traintxt_list)
            return traintxt


def create_im_and_grth(txt):
    # Textzeile werden in List-datei gesplittet
    lines = txt.splitlines()
    # Hier werden nur 1000 Zeilen berücksichtigt
    for l in range(1000):


        # Canvas erstellen
        bg = Image.new('RGB', (100, 2500), (255,255,255))

        # Font holen
        fnt = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc', 50)
        # Zeile auf dem Canvas schreiben
        d = ImageDraw.Draw(bg)
        d.text((25,30), lines[l], fill=(0,0,0), font=fnt, features=['kern', 'palt'], direction='ttb', language='ja')

        
        path1 = './traindata_2/text/'
        path2 = './traindata_2/image/'

        # Textzeile speichern
        txName = str(l+1) + '.gt.txt'

        with open(path1+txName, 'w') as f:
            print(lines[l], file=f)

        # Image speichern
        imName = str(l+1) + '.tif'
        bg.save(path2+imName)



if __name__ == '__main__':
    traintext = create_train_txt()
    create_im_and_grth(traintext)
