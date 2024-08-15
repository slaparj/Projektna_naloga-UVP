from bs4 import BeautifulSoup
import requests
import re

def dodatne_lastnosti(url_mange):
    
    html_mange = requests.get(url_mange)
    juha_mange = BeautifulSoup(html_mange.content, 'lxml')
    
    #Poiščemo kako popularna je manga
    popularnost_najdba = juha_mange.find('span', class_='numbers popularity')
    popularnost = int(''.join(re.findall(r'\d+', popularnost_najdba.text.strip()))) if popularnost_najdba else 'Popularity not found'
    
    #Poiščemo v katere žanre pripada manga
    seznam_zanrov = []
    zanri_naslov = juha_mange.find('span', string='Genres:') if juha_mange.find('span', string='Genres:') else juha_mange.find('span', string='Genre:') if juha_mange.find('span', string='Genre:') else 'Ne najdem žanrov'
    
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
        
    
    #Enako za tematike (ker so tematike in žanri na tej spletni strani malo pomešani)
    seznam_tematik = []
        
    if not juha_mange.find('span', string='Themes:') and not juha_mange.find('span', string='Theme:'):
        seznam_tematik = ['Nismo našli informacij']
    else:
        if juha_mange.find('span', string='Themes:'):
            tematike_naslov_naslov = juha_mange.find('span', string='Themes:')

        else:
            tematike_naslov_naslov = juha_mange.find('span', string='Theme:')
        bratec = zanri_naslov.next_sibling
        while bratec:
            seznam_tematik.append(bratec.text.strip())
            bratec = bratec.next_sibling
        
    seznam_tematik = list(dict.fromkeys(seznam_tematik))    
    if '' in seznam_tematik:
        seznam_tematik.remove('') 
    if ',' in seznam_tematik:  
        seznam_tematik.remove(',') 
        
        
    #Poiščemo še opis mange
    opisno_okno = juha_mange.find('span', itemprop='description')
    if opisno_okno:
        opis_vse = opisno_okno.text.strip().split('\n') 
        i = 0
        opis = ''
        while i < len(opis_vse) and 'Written by' not in opis_vse[i]:
            opis += opis_vse[i]
            i += 1
        opis = opis.replace('\r', '')
    else:
        opis = 'Description not found.'
    
        
    #Pridobljene podatke shranimo v slovar
    dodatni_podatki = {
        'popularnost': popularnost,
        'seznam_zanrov': seznam_zanrov,
        'tematike': seznam_tematik,
        'opis': opis
    }
    
    return dodatni_podatki