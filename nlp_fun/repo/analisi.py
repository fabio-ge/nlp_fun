from repo.calcola_indicatori import get_indicatori
from repo.util import pipe,estrai_parole,stem_parole,database
import nltk


class Filtro():

    def get_features(self,frase):
        """
        Calcolo il dizionario delle features.
        """
        def in_frase(parola,frase):
            if parola in frase:
                return 1
            else:
                return 0

        features = {}
        parole_stem = pipe([estrai_parole,stem_parole,set])(frase)
        for parola in self.indicatori:
            features[parola] = features.get(parola,0) + in_frase(parola,parole_stem)

        return features

    def costruisci_insiemi(self):
        feature_set = [(self.get_features(frase),label) for (frase,label) in database()]
        meta = int(len(feature_set)/2)
        train_set, test_set = feature_set[meta:],feature_set[:meta]
        return (train_set,test_set)
    
    def __init__(self):
        self.indicatori = pipe([stem_parole,set])(get_indicatori()) ## da materializzare, altrimenti ogni volta lo ricalcola
        train_set, _ = self.costruisci_insiemi()
        self.classificatore = nltk.NaiveBayesClassifier.train(train_set)
    
    def classifica(self,frase):
        return self.classificatore.classify(self.get_features(frase))

    def stampa_acc(self,set):
        return nltk.classify.accuracy(self.classificatore,set) 

if __name__ == '__main__':
    ## stemmo e trasformo in set gli indicatori
    filtro = Filtro()
    print(filtro.classifica('Sento una grande sofferenza e un grande dolore'))
    print(filtro.classifica('Sono felice')) 
    li1,li2 = filtro.costruisci_insiemi()
    print(filtro.stampa_acc(li2))