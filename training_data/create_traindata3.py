import random
import textwrap
from PIL import Image, ImageDraw, ImageFont

def create_train_txt():
    with open('/home/nobu/wiki_v3.txt') as f:
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
                #d = len(jpn_nums[m])
                t = new_text[m] + '︙'*10
                traintxt_list.append(t)

            traintxt = '\n'.join(traintxt_list)
            return traintxt, jpn_nums


def create_im_and_grth(txt, num_list):
    # Textzeile werden in List-datei gesplittet
    lines = txt.splitlines()
    nums = num_list

    # Hier werden nur 1000 Zeilen berücksichtigt
    for l in range(1000):

        # Für Textteil
        # Canvas erstellen
        bg = Image.new('RGB', (100, 2000), (255,255,255))
        # Font holen
        fnt = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc', 50)
        # Zeile auf dem Canvas schreiben
        d = ImageDraw.Draw(bg)
        d.text((25,30), lines[l], fill=(0,0,0), font=fnt, features=['kern', 'palt'], direction='ttb', language='ja')

        # Für die Kanji-Nums
        bg2 = Image.new('RGB', (100, 500), (255, 255, 255))
        d2 = ImageDraw.Draw(bg2)
        d2.text((25,30), nums[l], fill=(0,0,0), font=fnt, features=['kern', 'palt'], direction='ttb', language='ja')
        bg2_resize = bg2.resize((bg2.width, bg2.height // 2))

        img = Image.new('RGB', (bg.width, bg.height + bg2_resize.height))
        img.paste(bg, (0, 0))
        img.paste(bg2_resize, (0, bg.height))
        
        path1 = './traindata_3/text/'
        path2 = './traindata_3/image/'

        # Textzeile speichern
        txName = str(l+1) + '.gt.txt'

        with open(path1+txName, 'w') as f:
            print(lines[l] + nums[l], file=f)

        # Image speichern
        imName = str(l+1) + '.tif'
        img.save(path2+imName)



if __name__ == '__main__':
    traintext, nums_list = create_train_txt()
    create_im_and_grth(traintext, nums_list)