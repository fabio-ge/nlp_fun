from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from repo.util import estrai_parole,distribuzione,estrai_frasi
from repo.analisi import Filtro



app = Flask(__name__)
CORS(app)
filtro = Filtro()

@app.post("/gettext")
def get_text():
    url = request.get_json()['url']
    try:
        req = requests.get(url)
        testo = BeautifulSoup(req.text, 'html.parser').get_text()
        parole = estrai_parole(testo)
        frasi = estrai_frasi(testo)
        frasi_disagio = [frase for frase in frasi if filtro.classifica(frase) == 'SI']
        percent_disagio = int((len(frasi_disagio)/len(frasi))*100)
        vocabolario = len(set(parole))
        testo = len(parole)
        nome_img = distribuzione(parole) 
    
        return dict({"esito": "ok",
                     "frequenze": nome_img,
                     "frasi_disagio": frasi_disagio,
                     "percent_disagio": percent_disagio,
                     "vocabolario": vocabolario,
                     "testo": testo
                     })
    except Exception as e:
        return dict({"errore": f"Non trovo nulla all' url {url}"}) 


