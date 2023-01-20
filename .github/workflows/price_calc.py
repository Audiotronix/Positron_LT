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

def ceildiv(a, b):
    return -(a // -b)

def calc_real_price(part):
    factor = ceildiv(int(part['amount']), int(part['pcs']))
    price = float(part['price'].replace(',','.').replace('€','')) * factor
    return price

def calc_exact_price(part):
    single_price = float(part['price'].replace(',','.').replace('€','')) / int(part['pcs'])
    price = int(part['amount']) * single_price
    price = round(price, 2)
    return price

categories = {}
for part in in_csv:
    p = in_csv[part]
    
    if p['category'] not in categories:
        categories[p['category']] = {'real':0,'exact':0}
    categories[p['category']]['real'] += calc_real_price(p)
    categories[p['category']]['exact'] += calc_exact_price(p)

    #print(p['cad_name'], p['amount'], p['price'], p['pcs'], calc_real_price(p), calc_exact_price(p))

makerbeams = float(input('Makerbeams Price:').replace('€','').replace(',','.'))
for cat in categories:
    category = categories[cat]

    real = str(round(category['real'],2)).replace('.',',')
    exact = str(round(category['exact'],2)).replace('.',',')

    if cat == 'makerbeam':
        makerbeams_t = str(makerbeams).replace('.',',')
        real += f'€ + {makerbeams_t}'
        exact += f'€ + {makerbeams_t}'

        # needed for total
        category['real'] += makerbeams
        category['exact'] += makerbeams

    print(f'| {cat} | {real}€ | {exact}€ |')

real_total, exact_total = 0, 0
for cat in categories:
    real_total += categories[cat]['real']
    exact_total += categories[cat]['exact']

real_total = str(round(real_total,2)).replace('.',',')
exact = str(round(exact_total,2)).replace('.',',')

print('| | | |')
print(f'| Total | {real_total}€ | {exact_total}€ |')