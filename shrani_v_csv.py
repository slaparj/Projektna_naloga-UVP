import csv
import os

def shrani_v_csv(seznam):
    
    direktorij = 'csv_datoteke'

    if not os.path.exists(direktorij):
        os.makedirs(direktorij)
        
        csv_dat = 'manga_info.csv'
        
        dat_ime = os.path.join(direktorij, csv_dat)

    with open(dat_ime, mode='w', newline='', encoding='utf-8') as dat:
        writer = csv.DictWriter(dat, fieldnames=seznam[0].keys())
        writer.writeheader()
        writer.writerows(seznam)