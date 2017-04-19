import requests
from bs4 import BeautifulSoup
import pandas
import unicodedata

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

# p = Calendario 2017-A

url = "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta"

p = {"aulap": "", \
     "ciclop": "201710", \
     "crsep": "", \
     "cup": "D", \
     "edifp": "", \
     "horafp": "", \
     "horaip": "", \
     "majrp": "INCO", \
     "materiap": "", \
     "mostrarp": "1000", \
     "ordenp": "0"}

page = requests.post(url, params=p)
soup = BeautifulSoup(page.content)
items = soup.find_all("td", class_="tdprofesor")
nombre_profesor = []
materia = []
