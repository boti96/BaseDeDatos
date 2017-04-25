import requests
from bs4 import BeautifulSoup
import pandas
import unicodedata

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

# p = Calendario 2017-A



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

url = "http://consulta.siiau.udg.mx/wco/sspseca.consulta_oferta"
page = requests.post(url, params=p)
soup = BeautifulSoup(page.content)
items = soup.find_all("td", class_="tdprofesor") #nombre de Profesor
items2 = soup.find_all("a", href = True) #Nombre de la materiap
items3 = soup.find_all("td", class_="tddatos") #Sección
items4 = soup.find_all("td", class_="tddatos") #NRC
nombre_profesor = []
materia = []
ape1 = []
ape2 = []
sueldo_concatenate = []
sueldo_total = []
puesto = []
seccion = []
NRC = []

for x in items:
    if(x.text != "01"):
        if (x.text not in nombre_profesor):
            nombre_profesor.append(x.text)

            n = x.text
            n = n.replace(",", "")
            if ("NEGRON ADRIANA" in n):
                nombre_chido = n.rsplit(" ", 4)[3]
                ape1 = n.rsplit(" ", 4)[1]
                ape2 = n.rsplit(" ", 4)[0]
            elif ("FABIOLA DEL CARMEN" in n or "MARIA DEL SOCORRO" in n or \
                "SOTO SANCHEZ" in n or "BECERRA VELAZQUEZ" in n or \
                "VERA GOMEZ" in n or "BONILLA CARRANZA" in n or \
                "GUTIERREZ SALMERON" in n or "HERNANDEZ BARRAGAN" in n):

                #ecepciones de nombres muy largos

                nombre_chido = n.rsplit(" ", 4)[2]
                ape2 = n.rsplit(" ", 4)[0]
                ape1 = n.rsplit(" ", 4)[1]
            else:
                nombre_chido = n.rsplit(" ", 3)[2]
                ape1 = n.rsplit(" ", 3)[1]
                ape2 = n.rsplit(" ", 3)[0]

            if (not("Ñ" in nombre_chido)):
                nombre_chido = strip_accents(nombre_chido)

            if (not("Ñ" in ape1)):
                ape1 = strip_accents(ape1)

            if (not("Ñ" in ape2)):
                ape2 = strip_accents(ape2)

            p2 = {"pDepen": "", \
                  "pDepenDesc": "", \
                  "pMaterno": ape1.encode("iso-8859-1"), \
                  "pNombre": nombre_chido.encode("iso-8859-1"), \
                  "pPaterno": ape2.encode("iso-8859-1"), \
                  "pTabu": "", \
                  "p_selMes": "201703", \
                  "p_selMonto": "0", \
                  "p_selQui": "1"}

           url2 = "http://148.202.105.181/transd/ptqnomi_responsive.PTQNOMI_D"
           page2 = requests.post(url2, params=p2)
           soup2 = BeautifulSoup(page2.content)
           print(page2.url)

           if (soup2.text.count("$") <= 14):
               items2 = soup2.find_all("td", class_="td_beige")
               s1_temp = items2[8].text
               s1_temp = s1_temp.replace("$", "")
               s1_temp = s1_temp.replace(" ", "")
               s1_temp = s1_temp.replace(",", "")
               s2_temp = "$0.00"
               c1_temp = float(s1_temp)
               s1_temp = "$" + s1_temp + ", "
               s3_temp = c1_temp

               try:
                   sueldo_concatenate.append(s1_temp + s2_temp)
                   sueldo_total.append(s3_temp)
                   puesto.append(items2[2].text)
               except:
                   sueldo_concatenate.append(" ")
                   sueldo_total.append(" ")
                   puesto.append(" ")

            elif (soup2.text.count("$") > 14):
                items2 = soup2.find_all("td", class_="td_beige")
                items3 = soup2.find_all("td", class_="td_gris")
                if ((ape2 == "HERNANDEZ" and ape1 == "ANDRADE") or \
                    (ape2 == "MEZA" and ape1 == "ESPINOSA")):
                    s4_temp = items2[17].text
                    s1_temp = items2[8].text
                    s4_temp = s4_temp.replace("$", "")
                    s4_temp = s4_temp.replace(" ", "")
                    s4_temp = s4_temp.replace(",", "")
                    s1_temp = s1_temp.replace("$", "")
                    s1_temp = s1_temp.replace(" ", "")
                    s1_temp = s1_temp.replace(",", "")
                    s2_temp = items3[8].text
                    s2_temp = s2_temp.replace("$", "")
                    s2_temp = s2_temp.replace(" ", "")
                    s2_temp = s2_temp.replace(",", "")
                    c1_temp = float(s1_temp)
                    c2_temp = float(s2_temp)
                    c3_temp = float(s4_temp)
                    s1_temp = "$" + s1_temp + ", "
                    s2_temp = "$" + s2_temp + ", "
                    s4_temp = "$" + s4_temp
                    s3_temp = c1_temp + c2_temp + c3_temp
                    try:
                        sueldo_concatenate.append(s1_temp + s2_temp + s4_temp)
                        sueldo_total.append(s3_temp)
                        puesto.append(items2[2].text + ", " + items3[2].text)
                    except:
                        sueldo_concatenate
                        sueldo_total.append(" ")
                        puesto.apend(" ")
            else:
                    s1_temp = items2[8].text
                    s1_temp = s1_temp.replace("$", "")
                    s1_temp = s1_temp.replace(" ", "")
                    s1_temp = s1_temp.replace(",", "")
                    s2_temp = items3[8].text
                    s2_temp = s2_temp.replace("$", "")
                    s2_temp = s2_temp.replace(" ", "")
                    s2_temp = s2_temp.replace(",", "")
                    c1_temp = float(s1_temp)
                    c2_temp = float(s2_temp)
                    s1_temp = "$" + s1_temp + ", "
                    s2_temp = "$" + s2_temp
                    s3_temp = c1_temp + c2_temp
                    try:
                        sueldo_concatenate.append(s1_temp + s2_temp)
                        sueldo_total.append(s3_temp)
                        puesto.append(items2[2].text + ", " + items3[2].text)
                    except:
                        sueldo_concatenate.append(" ")
                        sueldo_total.append(" ")
                        puesto.apend(" ")

for y in items2:
    try:
        materia.append(y.text)
    except:
        materia.append(" ")

for z in items3:
    sec = z.text
    if(sec[1:1] == "D"):
        try:
            seccion.append(sec)
        except:
            seccion.append(" ")

for item_cont in items4:
    nrc__ = item_cont.text
    if(nrc__[1:1] != "I" and len(nrc__) == 5):
        try:
            NRC.append(nrc__)
        except:
            NRC.append(" ")


df = pandas.DataFrame(nombre_profesor, columns=['Nombre Profesor'])
df['Materia'] = materia
df['Seccion'] = seccion
df['Sueldos'] = sueldo_concatenate
df['Total Sueldo'] = sueldo_total

salida = open("SIIAU.html", 'w')
salida.write(df.to_html())
salida.close
