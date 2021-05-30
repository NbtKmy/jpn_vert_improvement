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

            while len(new_text) < 40000:
                add_txt = random.choice(wiki)
                new_text = new_text + add_txt

            
            traintxt = '\n'.join(textwrap.wrap(new_text, width=40))
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

        
        path1 = './traindata_1/text/'
        path2 = './traindata_1/image/'

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