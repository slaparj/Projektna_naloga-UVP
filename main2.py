import zajem
from shrani_v_csv import shrani

naj_nekaj = []


#spletna stran prikaže po 50 zaporednih mang, na vsaki spletni strani poženemo funkcijo izlusci()  
for i in range(2):
    if i == 0:
        url = 'https://myanimelist.net/topmanga.php'
    else: 
        url = f'https://myanimelist.net/topmanga.php?limit={i * 50}'
        
    naj_nekaj.extend(zajem.dodatno(url))

print(naj_nekaj)
shrani(naj_nekaj, 1)