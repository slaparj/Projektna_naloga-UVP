from zajem import izlusci
from zajem2 import dodatne_lastnosti

naj_mange = []


#spletna stran prikaže po 50 zaporednih mang, na vsaki spletni strani poženemo funkcijo izlusci()  
for i in range(2):
    if i == 0:
        url = 'https://myanimelist.net/topmanga.php'
    else: 
        url = f'https://myanimelist.net/topmanga.php?limit={i * 50}'
    naj_mange.extend(izlusci(url))
    print(naj_mange)


for i in range(1):
    url_mange = naj_mange[i]['link']
    print(dodatne_lastnosti(url_mange))
    