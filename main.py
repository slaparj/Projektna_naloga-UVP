import zajem

naj_mange = []


#spletna stran prikaže po 50 zaporednih mang, na vsaki spletni strani poženemo funkcijo izlusci()  
for i in range(1):
    if i == 0:
        url = 'https://myanimelist.net/topmanga.php'
    else: 
        url = f'https://myanimelist.net/topmanga.php?limit={i * 50}'
    naj_mange.extend(zajem.izlusci(url))

print(naj_mange)
    