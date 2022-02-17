import nltk
from repo.util import estrai_parole,pipe,argomenti

def get_parole(nome_file):
    with open(nome_file,'r') as f:
        righe = list(f.readlines())
        return [estrai_parole(riga)for riga in righe]

def shallow_flatten(li):
    new_li = []
    for i in li:
        for j in i:
            new_li.append(j)
    
    return new_li

def prime_10(parole):
    return nltk.FreqDist(parole).most_common(10)

def get_first(l):
    return [el[0] for el in l]

def get_indicatori():
    indicatori = []
    for argomento in argomenti:
        indicatori.append((pipe([get_parole,shallow_flatten,prime_10,get_first])(f'frasi_{argomento}.txt')))
    risultato = pipe([shallow_flatten,set])(indicatori)
    return risultato

if __name__ == '__main__':
    print(get_indicatori)    