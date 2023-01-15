import csv

in_csv = {}
try:
    with open('./Parts/bom.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            if row['amount'] in ['','---','-->'] or row['price'] in ['','---','-->'] or row['pcs'] in ['','---','-->']: continue

            in_csv[row['cad_name']] = row
except:
    pass

def calc_real_price(part):
    pass

def calc_exact_price(part):
    pass

for part in in_csv:
    p = in_csv[part]
    print(p['cad_name'], p['amount'], p['price'], p['pcs'])