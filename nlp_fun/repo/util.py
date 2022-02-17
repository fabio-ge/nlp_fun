import nltk
from functools import reduce
import random
from os import listdir
import numpy as np
import matplotlib.pyplot as plt


stemmer = nltk.stem.SnowballStemmer('italian')
my_stop_words = ['può','sempre','modo','quando','stesso','senza','ogni','tempo','dopo','fatto','così','cosa','ora','poi']
argomenti = ['conflitti','delusioni','fallimento','inquietudine','odio','sofferenza']
stopwords = nltk.corpus.stopwords.words("italian")

def get_index(s):
    nome = s.split('.')[0]
    indice = int(nome.split('-')[1])
    return indice

def new_img():
    nome = sorted(listdir('img'),key=get_index)[-1]
    indice = get_index(nome)
    indice += 1
    return f'img/pie-{indice}.png'



def distribuzione(lista_parole):
    fd = nltk.FreqDist(lista_parole)
    piu_comuni = fd.most_common(10)
    nome = new_img()
    valori = [coppia[1] for coppia in piu_comuni]
    label = [coppia[0] for coppia in piu_comuni]
    x = np.array(valori)
    plt.switch_backend('agg')
    plt.pie(x,labels=label)
    plt.savefig(nome,transparent=True)
    plt.clf()
    
    return nome


def estrai_frasi(testo):
    return nltk.sent_tokenize(testo)


def stem_parole(lista_parole):
    """
    Mappo ogni parola della lista nel suo stem
    """
    return [stemmer.stem(parola) for parola in lista_parole]

def pipe(lista_fn):
    return lambda input: reduce(lambda input,fn: fn(input),lista_fn,input)

def estrai_parole(testo):
    """
    Dato un testo, produco una lista delle sole parole utili all' analisi
    """
    tokens = nltk.word_tokenize(testo)
    # rimuovo punteggiatura
    parole = [w for w in tokens if w.isalpha()]
    parole_utili = [w.lower() for w in parole if w.lower() not in stopwords]
    parole_utili = [parola for parola in parole_utili if parola not in my_stop_words]
    parole_utili = [w for w in parole_utili if len(w) > 2]    
    return parole_utili

def appendi_frasi(nome_file,label,lista):
    with open(nome_file) as f:
            for line in f.readlines():
                lista.append((line,label))


def mischia_lista(li):
    random.shuffle(li)
    return li

def get_frasi():
    frasi = []
    for argomento in argomenti:
        appendi_frasi(f'frasi_{argomento}.txt','SI',frasi)
    #appendo le frasi positive dal file felicita
    appendi_frasi('frasi_felicita.txt','NO',frasi)        
    return frasi

def database():
    return mischia_lista(get_frasi())

if __name__ == '__main__':
    pass
    #test di alcune funzioni
    ##print(len(database()))
    ##print(estrai_parole('Cerca il testo ad un determinato link, e vediamo che umore ne esce'))
    # print(new_img())