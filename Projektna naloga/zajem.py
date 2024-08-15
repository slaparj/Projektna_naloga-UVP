from bs4 import BeautifulSoup
import requests
import re

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
    
        #popularnost_najdba = re.search(r'Popularity #(\d+)', podatki_text)
        deli_najdba = re.search(r'(\d+) vols', podatki_text)
    
        #popularnost = popularnost_najdba.group(1) if popularnost_najdba else 'N/A'
        deli = deli_najdba.group(1) if deli_najdba else 'Ni končana'
    
        lastnosti_mange = {
            'rank': rank,
            'naslov': naslov,
            'link': link,
            'ocena': ocena,
            'deli': deli,
            #'popularnost': popularnost,
            #'zanri': zanri,
            #'opis': opis
        }
        
        print(f'{rank}. {naslov}, {ocena} {deli}')
        seznam_mang.append(lastnosti_mange)
    return seznam_mang
