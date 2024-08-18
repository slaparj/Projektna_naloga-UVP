from bs4 import BeautifulSoup
import requests
import re
from zajem2 import dodatne_lastnosti

def izlusci(url):
    
    seznam_mang = []
    
    html = requests.get(url)
    juha = BeautifulSoup(html.content, 'lxml')
    mange = juha.find_all('tr', class_="ranking-list")
    
    for manga in mange:
        
        #najdemo osnovne podatke
        naslov = manga.h3.text.strip()
        rank = manga.span.text.strip()
        ocena = manga.find('td', class_="score").text.strip()
        link = manga.find('a')['href']
    
        #iščemo še podatke shranjene v dodatnem 'hover oblačku'
        podatki = manga.find('div', class_='information di-ib mt4')
        podatki_text = podatki.text.strip().replace('\n', ' ')
    
        deli_najdba = re.search(r'(\d+) vols', podatki_text)
    
        deli = deli_najdba.group(1) if deli_najdba else 'Ni končana'
    
        lastnosti_mange = {
            'rank': rank,
            'naslov': naslov,
            'ocena': ocena,
            'deli': deli,
        }
        
        dodatni_seznam = dodatne_lastnosti(link)
        
        lastnosti_mange.update(dodatni_seznam)
        
        #print(f'{rank}. {naslov}, {ocena} {deli}')
        seznam_mang.append(lastnosti_mange)
        
    return seznam_mang
