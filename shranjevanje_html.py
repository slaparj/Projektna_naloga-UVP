import os
import requests

direktorij = 'html_datoteke'

if not os.path.exists(direktorij):
    os.makedirs(direktorij)


for i in range(20):
    
    if i == 0:
        url = 'https://myanimelist.net/topmanga.php'
    else: 
        url = f'https://myanimelist.net/topmanga.php?limit={i * 50}'
    
    html = requests.get(url)

    dat_ime = os.path.join(direktorij, f'html_datoteka{i + 1}.html')

    # Save the HTML content to a file
    with open(dat_ime, 'w', encoding='utf-8') as file:
        file.write(html.text)

    print(f'Saved: {dat_ime}')