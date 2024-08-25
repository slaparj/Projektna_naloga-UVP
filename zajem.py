from bs4 import BeautifulSoup
import requests
import re
import time

#Funkcija, ki bo iz glavne spletne strani pobrala mange: rank, naslov, ocena in število delov
def izlusci(url):
    
    #Prazen seznam, v katerega bomo dodajali mange
    seznam_mang = []
    
    
    #Pošljemo request spletni strani, zaradi težav pri nalaganju sem dodal še time.sleep() zakasnitev
    html = requests.get(url)
    time.sleep(5)
    
    #Dobimo html
    juha = BeautifulSoup(html.content, 'lxml')
    mange = juha.find_all('tr', class_="ranking-list")
    
    for manga in mange:
        
        #najdemo osnovne podatke
        naslov = manga.h3.text.strip()
        rank = manga.span.text.strip()
        ocena = manga.find('td', class_="score").text.strip()
    
    
    
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

        #Dodamo vsako mango v seznam
        seznam_mang.append(lastnosti_mange)
        
        
    return seznam_mang


#Ta funkcija podobno kot prva najde osnovne podatke, le da poišče še link vsake mange in za vsako požemne funkcijo dodatne_lastnosti()
def dodatno(url):
    
    seznam_mang = []
    
    html = requests.get(url)
    print(html.status_code)
    time.sleep(5)
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
        #print(f'{rank}, {naslov}, {ocena}, {deli}')
        seznam_mang.append(lastnosti_mange)
        

    return seznam_mang


#funkcija, ki vsaki mangi poišče dodatne lastnosti. To stori, tako da obišče link vsake mange posebaj in izlušči popularnost, seznam žanrov in revijo, ki mango objavlja
def dodatne_lastnosti(url_mange):
    
    
    html_mange = requests.get(url_mange)
    print(html_mange.status_code)
    time.sleep(5)
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
        'žanri': seznam_zanrov,
        'revija': revija
    }
    
    return dodatni_podatki