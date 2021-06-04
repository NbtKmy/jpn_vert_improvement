# Verbessrungsversuch des jpn_vert-Modells für tesseract

In diesem Repo befinden sich die Codes und Daten für das Training von jpn_vert (best).
Für die Vorarbeitung nehme ich die Python-Code, die ich in dem [anderen Repo](https://github.com/NbtKmy/tesseract_jpn-vert) verwendet habe.  

Presentation: https://nbtkmy.github.io/jpn_vert_improvement/presentation/reveal/index.html

# Dokumentation zur Erstellung der Trainingdaten

Grob gesagt, sind die Trainingsdaten aus Wikipedia-Texte und Werktitel der [Authoritätsdaten der japanischen National Diet Library](https://id.ndl.go.jp/auth/ndla) entstanden.  
Die Textdaten werden zunächst aus diesen beiden Quellendaten erzeugt. Die Texte werden in einzelnen Zeilen aufgeteilt. Aus diesen Zeilen werden die Bilder erstellt.  

## Trainingsdaten aus den Wikipedia-Texten (Japanisch) herstellen

1. Der gesamte Wikipedia-Text (Japanisch) als ein Dump-File herunterladen  

URL: <https://dumps.wikimedia.org/jawiki/latest/>  
Auf dieser Seite findet man das aktuelle Dump-File vom gesamten japanischsprachigen Wikipedia-Text:  

`jawiki-latest-pages-articles.xml.bz2               01-May-2021 20:18          3360581573`

Die Daten wird im bz2-Format heruntergeladen. Wenn sie entpackt wird, sieht man, dass der Inhalt in xml-Format geschrieben ist (14 GB...):  

`jawiki-latest-pages-articles.xml`


2. Eine passende Text-Daten aus dem xml-File erstellen

Um die Text-Teile aus dem xml-File herauszuholen, wird [WikiExtractor](https://github.com/attardi/wikiextractor) verwendet.  
Installation:  
`pip install wikiextractor`  
Exstraktion der Text-Teile:  
`python -m wikiextractor.WikiExtractor jawiki-latest-pages-articles.xml`


Die extrahierten Textteile sind in zahlreichen kleinen Textdaten gespeichert. Diese Textdaten werden durch den folgenen Befehl in eine einzige Textdaten zusammengefasst:  

`find text/ | grep wiki | awk '{system("cat "$0" >> wiki.txt")}'`

Das Text-File enthält immer noch unnötige Zeile mit Doc-Tag. Diese werden gelöscht:  

`sed -i '/^<[^>]*>$/d' wiki.txt`  

Leere Zeile werden eliminiert:  

`sed -i '/^$/d' wiki.txt`

Die sich häufig wiederholgenden kleineren Überschriften wie "概要.(= Zusammenfassung)" (immer "."-Zeichen am Zeilen-Ende) gelöscht:  
`sed -e '/\.$/d' ./wiki.txt > ./wiki_v2.txt`

Nach jedem Punkt "。" wird ein Zeilenumbruch hineingeschoben.  
`sed -e 's/。/。\n/g' ./wiki_v2.txt | sed -e '/^$/d' > ./wiki_v3.txt`

Im File "wiki_v3.txt" sind alle Sätze und (sinnvollere) Überschriften jeweils in einer Zeile unterbracht. 

## Werktitel aus Web NDL Authorities sammeln

NDL-Authorities erlaubt den Zugriff auf die Daten durch SPARQL-Query.  
Die ausführliche Information über SPARQL-Query ist auf der Webseite von [Web NDL Authorities](https://id.ndl.go.jp/information/sparql/) zu sehen.
Um alle mögliche Werktitle herauszufiltern, ist die Python-Code [./training_data/ndl_sparql.py](https://github.com/NbtKmy/jpn_vert_improvement/blob/main/training_data/ndl_sparql.py) geschrieben.  
Dabei ist die Python library [SparqlWrapper](https://github.com/RDFLib/sparqlwrapper) verwendet.

Die so gesammelten Werktitel sind in [./training_data/titelList.txt](https://github.com/NbtKmy/jpn_vert_improvement/blob/main/training_data/titleList.txt) zu finden.


## Erstellung der Trainingsdaten
In diesem Projekt sind drei Sets der Trainingsdaten erstellt. 
Das erste Set besteht aus reinem Text, für den die Wikipedia-Texte und Werktitel gemischt worden sind. 

Bei dem zweiten Set ist die Struktur des japanischsprachigen Inhaltsverzeichnis berücksichtigt und die fiktiven Seitenzahl und das Füllzeichen '︙' hinzugefügt. 

<img src="https://nbtkmy.github.io/jpn_vert_improvement/presentation/89.png" width="50px">


```
渡暦月9%を刑罰法令の適用の上限金利（民事上の上限であるかに︙︙︙︙︙︙︙︙︙七
```


Bei dem dritten Set sind lediglich die Darstellung der Zahlen in Chinesischer Schrift vertikal verkleinert, so wie sie in einem realen Inhaltsverzeichnis gefunden wird.

<img src="https://nbtkmy.github.io/jpn_vert_improvement/presentation/57.png" width="50px">


Jedes Set enthält 1000 Paare von Bilddatei (.tif) und Textdatei (.gt.txt).  


## Erstellung der Word- und Puncliste

Unter [langdata_lstm](https://github.com/tesseract-ocr/langdata_lstm) findet man die word-, punc- und numbers-Liste.
Für das Training können diese Liste verwendet werden.
Bei jpn_vert ist die numbers-Liste jedoch leer.

In der punc-Liste sind ausschliesslich die "Halfwidth"-Zeichen. Es sind keine speziellen Satzzeichen.
In der word-Liste sind viele Wörter zu finden. 

In diesem Repo sind eine neue punc-Liste erstellt, die japanisch-speziellen Satzzeichen (Fullwidth) aufgenommen sind (mit der [Python-Code](https://github.com/NbtKmy/jpn_vert_improvement/blob/main/training_data/lstm_dict/create_Punclist.py)).
Word-Liste habe ich mit der Liste der Werktitel aus der NDL-Auth erweitert (mit der [Python-Code](https://github.com/NbtKmy/jpn_vert_improvement/blob/main/training_data/lstm_dict/create_Wordlist.py)). 

Die neu erstellten Liste sind [hier](https://github.com/NbtKmy/jpn_vert_improvement/tree/main/training_data/lstm_dict) zu finden.

## Training mit Tesstrain
Für das Training wurde [tesstrain](https://github.com/tesseract-ocr/tesstrain) verwendet. 
So wie in README von tesstrain steht, wurde zuerst "tesseract built with the training tools and matching leptonica bindings" installiert.
Tesstrain braucht noch folgende Python Libraries:

* Pillow>=6.2.1
* python-bidi>=0.4
* matplotlib
* pandas

Das Repo tesstrain clonen:

`$ git clone https://github.com/tesseract-ocr/tesstrain.git`

...und nach der Erläuterung von tesstrain packt man die div. Daten unter dem tesstrain-Ordner:

* Start-Modell, das fine getunt werden soll, unter ./usr/share/tessdata/
* Ground-Truth-Daten (Texte und Image) unter ./data/[Name des Modells]-ground-truth

Dann unter dem Ordner tesstrain den Befehl eingeben:

`$ nohup time -f "Run time = %E\n" make training MODEL_NAME=jpn_vert START_MODEL=jpn_vert PSM=5 >> train.log 2>&1 &`

PSM=5 ist für jpn_vert notwendig...

Um die log-Daten zu checken

`$ tail -f train.log`

## Trainingsverfahren



