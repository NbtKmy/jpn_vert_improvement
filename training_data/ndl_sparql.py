from SPARQLWrapper import SPARQLWrapper
import math
import re

def ndlAuthQuery():
    sparql = SPARQLWrapper(endpoint='https://id.ndl.go.jp/auth/ndla', returnFormat='json')
    sparql.setQuery('''
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rda: <http://RDVocab.info/ElementsGr2/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    PREFIX xl: <http://www.w3.org/2008/05/skos-xl#>
    PREFIX ndl: <http://ndl.go.jp/dcndl/terms/>
    PREFIX dct: <http://purl.org/dc/terms/>
    SELECT DISTINCT (COUNT(?title) AS ?howmany) WHERE {
    {
    ?uri1 skos:inScheme <http://id.ndl.go.jp/auth#uniformTitles>.
    ?uri1 xl:prefLabel [ xl:literalForm ?title]. 
    OPTIONAL {
    ?uri1 xl:altLabel [ xl:literalForm ?alttitle]. 
    }
    ?uri1 dct:source '国書総目録'.
    } UNION {
    ?uri1 skos:inScheme <http://id.ndl.go.jp/auth#uniformTitles> ; skos:relatedMatch ?link2.
    ?uri1 xl:prefLabel [ xl:literalForm ?title]. 
    OPTIONAL {
    ?uri1 xl:altLabel [ xl:literalForm ?alttitle]. 
    }
    FILTER regex(?link2, '^.*KG.*')
    } UNION {
    ?uri1 skos:inScheme <http://id.ndl.go.jp/auth#work> ; skos:exactMatch ?link.
    ?uri1 xl:prefLabel [ xl:literalForm ?title]. 
    OPTIONAL {
    ?uri1 xl:altLabel [ xl:literalForm ?alttitle]. 
    }
    FILTER regex(?link, '^http.*nijl.*')
    } UNION {
    ?uri1 skos:inScheme <http://id.ndl.go.jp/auth#uniformTitles>.
    ?uri1 xl:prefLabel [ xl:literalForm ?title]. 
    OPTIONAL {
    ?uri1 xl:altLabel [ xl:literalForm ?alttitle]. 
    }
    ?uri1 dct:source ?x.
    FILTER regex(?x, '^日本古典籍総合目録.*')
    }
    }
    ''')
    res = sparql.query().convert()
    x = res['results']['bindings']
    TitleNum = 0
    for i in x:
        y = i['howmany']['value']
        TitleNum += int(y)
    
    if TitleNum > 100:
        itl = math.ceil(TitleNum / 100)
    else:
        itl = 1
    
    TitleList = []
    for l in range(itl):
        m = l + 1
        q = '''
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rda: <http://RDVocab.info/ElementsGr2/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX xl: <http://www.w3.org/2008/05/skos-xl#>
        PREFIX ndl: <http://ndl.go.jp/dcndl/terms/>
        PREFIX dct: <http://purl.org/dc/terms/>
        SELECT DISTINCT ?title ?alttitle WHERE {
        {
        ?uri1 skos:inScheme <http://id.ndl.go.jp/auth#uniformTitles>.
        ?uri1 xl:prefLabel [ xl:literalForm ?title]. 
        OPTIONAL {
        ?uri1 xl:altLabel [ xl:literalForm ?alttitle]. 
        }
        ?uri1 dct:source '国書総目録'.
        } UNION {
        ?uri1 skos:inScheme <http://id.ndl.go.jp/auth#uniformTitles> ; skos:relatedMatch ?link2.
        ?uri1 xl:prefLabel [ xl:literalForm ?title]. 
        OPTIONAL {
        ?uri1 xl:altLabel [ xl:literalForm ?alttitle]. 
        }
        FILTER regex(?link2, '^.*KG.*')
        } UNION {
        ?uri1 skos:inScheme <http://id.ndl.go.jp/auth#work> ; skos:exactMatch ?link.
        ?uri1 xl:prefLabel [ xl:literalForm ?title]. 
        OPTIONAL {
        ?uri1 xl:altLabel [ xl:literalForm ?alttitle]. 
        }
        FILTER regex(?link, '^http.*nijl.*')
        } UNION {
        ?uri1 skos:inScheme <http://id.ndl.go.jp/auth#uniformTitles>.
        ?uri1 xl:prefLabel [ xl:literalForm ?title]. 
        OPTIONAL {
        ?uri1 xl:altLabel [ xl:literalForm ?alttitle]. 
        }
        ?uri1 dct:source ?x.
        FILTER regex(?x, '^日本古典籍総合目録.*')
        }
        } LIMIT 100
        '''

        if m == 1 :
            sparql.setQuery(q)
        else:
            q = q + ' OFFSET ' + str(l*100)
            sparql.setQuery(q)
        
        res2 = sparql.query().convert()
        
        for n in res2['results']['bindings']:
            t1 = n['title']['value']
            t1 = re.sub('--.*', '', t1)
            t1 = re.sub(' \(.*', '', t1)
            TitleList.append(t1)

            if n.get('alttitle') is None:
                continue
            else:
                t2 = n['alttitle']['value']
                t2 = re.sub('--.*', '', t2)
                t2 = re.sub(' \(.*', '', t2)
                TitleList.append(t2)
            
        
    titLis = list(set(TitleList))
    print ('Es sind ' + str(len(titLis)) + ' Titel!')
    ListTxt = '\n'.join(titLis)

    with open('./titleList.txt', mode='w') as f:
        f.write(ListTxt)


if __name__ == '__main__':
    ndlAuthQuery()