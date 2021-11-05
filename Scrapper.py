from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import numpy as np
import pandas as pd
import time
from random import random

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
headers2 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
html = 0

start1 = open(r'D:\Git\Estudos\Jrpgs\Start.txt', "r")
stop1 = open(r'D:\Git\Estudos\Jrpgs\Stop.txt', "r")

start = start1.read()
start1.close()
stop = stop1.read()
stop1.close()
start = int(start)
stop = int(stop)

cod_id = np.arange(start,stop,1)
start = str(stop)
stop = stop+3000
stop = str(stop)
df = pd.DataFrame()

def BuscaJogo(valor):
    teste = False
    url = 'https://howlongtobeat.com/game?id='+str(valor)
    try:
        req = Request(url, headers=headers)
        response = urlopen(req)
        html = response.read()
        teste = True
    except HTTPError as e:
        #print(e.status, e.reason)
        teste = False
    except URLError as e:
        #print(e.reason)
        teste = False
        
    if teste:
        try:
            html = html.decode('utf-8')
            html = " ".join(html.split()).replace('> <','><')
            return html
        except:
            return 'NAN'
    else:
        return 'NAN'

for i in cod_id:
    soup = BeautifulSoup(BuscaJogo(i), 'html.parser')
    if soup.getText() == 'NAN':
        pass
    else:
        try:
            id_add = i

        except:
            id_add = 'NAN'

        try:
            Name_add = soup.find_all(class_="profile_header shadow_text")[0].getText()

        except:
            Name_add = 'NAN'


        try:
            Main_Story_add = soup.find(class_="game_times").find_all('li')[0].getText().replace(soup.find(class_="game_times").find_all('h5')[0].getText(),'')
        except:
            Main_Story_add = 'NAN'

        try:
            Main_Extras_add = soup.find(class_="game_times").find_all('li')[1].getText().replace(soup.find(class_="game_times").find_all('h5')[1].getText(),'')
        except:
            Main_Extras_add = 'NAN'

        try:
            Completionist_add = soup.find(class_="game_times").find_all('li')[2].getText().replace(soup.find(class_="game_times").find_all('h5')[2].getText(),'')
        except:
            Completionist_add = 'NAN'

        try:
            All_Styles_add = soup.find(class_="game_times").find_all('li')[3].getText().replace(soup.find(class_="game_times").find_all('h5')[3].getText(),'')
        except:
            All_Styles_add = 'NAN'


        try:
            soup.find_all(class_="profile_info")
            teste = True
        except:
            teste = False


        Plataforms_add = 'NAN'
        Genre_add = 'NAN'
        Developer_add = 'NAN'
        Publisher_add = 'NAN'
        NA_add = 'NAN'
        EU_add = 'NAN'
        JP_add = 'NAN'

        if teste:
            for j in soup.find_all(class_="profile_info"):
                if j.getText().count('Platforms:'):
                    Plataforms_add = j.getText().replace('Platforms:', '')
                elif j.getText().count('Genre:'):
                    Genre_add = j.getText().replace('Genre:', '')
                elif j.getText().count('Developer:'):
                    Developer_add = j.getText().replace('Developer:', '')
                elif j.getText().count('Publisher:'):
                    Publisher_add = j.getText().replace('Publisher:', '')
                elif j.getText().count('NA:'):
                    NA_add = j.getText().replace('NA:', '')
                elif j.getText().count('EU:'):
                    EU_add = j.getText().replace('EU:', '')
                elif j.getText().count('JP:'):
                    JP_add = j.getText().replace('JP:', '')
                else:
                    pass


        biblio = {
        'id': id_add,
        'Name': Name_add,
        'Main Story': Main_Story_add,
        'Main + Extras': Main_Extras_add,
        'Completionist': Completionist_add,
        'All Styles': All_Styles_add,
        'Platforms':Plataforms_add,
        'Genre':Genre_add,
        'Developer':Developer_add,
        'Publisher':Publisher_add,
        'NA':NA_add,
        'EU':EU_add,
        'JP':JP_add}

        df = df.append(biblio, ignore_index = True)
        time.sleep(random()/2)

        if i%10 == 0:
            time.sleep(random()/2)

        print(i)


df.to_csv(r'D:\Git\Estudos\Jrpgs\Dados\out'+start+'.csv',sep=';')

start1 = open(r'D:\Git\Estudos\Jrpgs\Start.txt', "w")
stop1 = open(r'D:\Git\Estudos\Jrpgs\Stop.txt', "w")
start1.write(start)
start1.close()
stop1.write(stop)
stop1.close()



