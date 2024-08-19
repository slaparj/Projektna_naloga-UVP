from bs4 import BeautifulSoup
import requests
import re

def dodatne_lastnosti(url_mange):
    
    html_mange = requests.get(url_mange)
    juha_mange = BeautifulSoup(html_mange.content, 'lxml')
    
    #Poiščemo kako popularna je manga
    popularnost_najdba = juha_mange.find('span', class_='numbers popularity')
    popularnost = int(''.join(re.findall(r'\d+', popularnost_najdba.text.strip()))) if popularnost_najdba else 'Nismo našli popularnosti'
    
    #Poiščemo v katere žanre pripada manga
    seznam_zanrov = []
    #zanri_naslov = juha_mange.find('span', string='Genres:') if juha_mange.find('span', string='Genres:') else juha_mange.find('span', string='Genre:') if juha_mange.find('span', string='Genre:') else 'Ne najdem žanrov'
    
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

    print(f'{popularnost}, {seznam_zanrov}, {revija}')
    
    return dodatni_podatki

dodatne_lastnosti('https://myanimelist.net/manga/51/Slam_Dunk')