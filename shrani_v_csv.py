import csv
import os

def shrani(seznam, n=0):
    
    direktorij = 'csv_datoteke'

    if not os.path.exists(direktorij):
        os.makedirs(direktorij)
        
    if n == 0:    
        csv_dat = 'manga_info.csv'
    else:
        csv_dat = 'manga_info2.csv'
        
    dat_ime = os.path.join(direktorij, csv_dat)

    with open(dat_ime, mode='w', newline='', encoding='utf-8') as dat:
        writer = csv.DictWriter(dat, fieldnames=seznam[0].keys())
        writer.writeheader()
        writer.writerows(seznam)