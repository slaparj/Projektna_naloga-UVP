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
    
    
    
        #najdemo še število poglavij
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
        
    
        #temu slovarju dodamo še slovar dodatnik podatkov, ki ga najde funkcija 'dodatni_podatki'
        dodatni_seznam = dodatne_lastnosti(link)
        lastnosti_mange.update(dodatni_seznam)
        
        #print(f'{rank}. {naslov}, {ocena} {deli}')
        seznam_mang.append(lastnosti_mange)
        
    return seznam_mang



#funkcija, ki vsaki mangi poišče dodatne lastnosti. To stori, tako da obišče link vsake mange posebaj in izlušči popularnost, seznam žanrov in revijo, ki mango objavlja
def dodatne_lastnosti(url_mange):
    
    html_mange = requests.get(url_mange)
    juha_mange = BeautifulSoup(html_mange.content, 'lxml')
    
    
    
    #Poiščemo kako popularna je manga
    popularnost_najdba = juha_mange.find('span', class_='numbers popularity')
    popularnost = int(''.join(re.findall(r'\d+', popularnost_najdba.text.strip()))) if popularnost_najdba else 'Nismo našli popularnosti'
    
    
    
    #Poiščemo v katere žanre pripada manga
    seznam_zanrov = []
    
    if not juha_mange.find('span', string='Genres:') and not juha_mange.find('span', string='Genre:'):
        seznam_zanrov = ['Nismo našli informacij']
    else:
        if juha_mange.find('span', string='Genres:'):
            zanri_naslov = juha_mange.find('span', string='Genres:')

        else:
            zanri_naslov = juha_mange.find('span', string='Genre:')
        bratec = zanri_naslov.next_sibling
        while bratec:
            seznam_zanrov.append(bratec.text.strip())
            bratec = bratec.next_sibling
        
    seznam_zanrov = list(dict.fromkeys(seznam_zanrov))    
    if '' in seznam_zanrov:
        seznam_zanrov.remove('') 
    if ',' in seznam_zanrov:  
        seznam_zanrov.remove(',') 
    
    
    
    #Najdimo še, v kateri reviji je manga objavljena
    revija_najdba = juha_mange.find('span', class_='information season')
    revija = revija_najdba.a.text.strip() if revija_najdba else 'Nismo našli revije'
    
    
    
    #Pridobljene podatke shranimo v slovar
    dodatni_podatki = {
        'popularnost': popularnost,
        'seznam_zanrov': seznam_zanrov,
        'revija': revija
    }

    #print(f'{popularnost}, {seznam_zanrov}, {revija}')
    
    return dodatni_podatki