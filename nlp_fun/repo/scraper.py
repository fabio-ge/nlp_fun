import requests
from bs4 import BeautifulSoup

URL = 'https://www.frasicelebri.it/argomento/'

def formatta(str):
    """
    @input str è della forma "frase."Autore
    Mi interessa estrarre solo la frase
    """
    pezzi = str.split('.')
    prima_parte = pezzi[0]
    frase = prima_parte[1:]
    return frase

def get_frasi_from_page(soup):
    frasi = soup.find_all('div', class_="post-box")
    frasi = [frase.find('blockquote').text for frase in frasi]
    frasi = [formatta(frase) for frase in frasi]
    return frasi

if __name__ == '__main__':
    nome = 'odio'
    pagine = 25
    url = f"{URL}{nome}/?page="
    for i in range(1,pagine+1):
        try:
            page = requests.get(f"{url}{i}")
            soup = BeautifulSoup(page.content,'html.parser',from_encoding="utf-8")
            frasi = get_frasi_from_page(soup)
            with open(f"frasi_{nome}.txt",'a') as f:
                f.write('\n'.join(frasi))    
        except UnicodeEncodeError:
            print(f'Salto la pagina{i}')
