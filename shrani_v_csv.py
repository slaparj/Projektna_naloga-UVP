import csv

def shrani_v_csv(seznam):

    csv_dat = 'manga_info.csv'

    with open(csv_dat, mode='w', newline='', encoding='utf-8') as dat:
        writer = csv.DictWriter(dat, fieldnames=seznam[0].keys())
        writer.writeheader()
        writer.writerows(seznam)