print('-FORMATTING BOM .csv')

import csv, collections, re

def remove_lang_link(text):
    return re.sub('(?<=https://)(.*)(?=aliexpress.com)','',text,flags=re.DOTALL)

def write_part_to_csv(name, this_part, old_part, writer):
    writer.writerow({
        'type': this_part['type'],
        'category': old_part.get('category', ''),
        'cad_name': name,
        'amount': this_part.get('amount',''),
        'price': old_part.get('price', '---'),
        'pcs': old_part.get('pcs', '---'),
        'link': remove_lang_link(old_part.get('link', '---')),
        'alt_link': remove_lang_link(old_part.get('alt_link', '---')),
        'note': remove_lang_link((str(this_part.get('note','')) if old_part.get('note','') == '' else str(old_part.get('note',''))))
        })

in_csv = {}
try:
    with open('./Parts/bom.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
                if row['type'] != '':
                    name = row['cad_name']

                    if row['cad_name'] == '' and row['type'] == 'category_info':
                        name = row['category'] + row['type']

                    in_csv[name] = row
except:
    pass

parts = in_csv

# create csv
csvfile = open('./Parts/bom.csv', 'w', newline='', encoding='utf-8')
fieldnames = ['type', 'category', 'cad_name', 'amount', 'price', 'pcs', 'link', 'alt_link', 'note']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')

writer.writeheader()

categories = {}
for part in in_csv:
    if in_csv[part]['category'] not in categories and in_csv[part]['category'] != '':
        if in_csv[part]['type'] == 'category_info': continue 
        categories[in_csv[part]['category']] = in_csv[part]['type']

categories = collections.OrderedDict(sorted(categories.items()))  # sort cats

parts = collections.OrderedDict(sorted(parts.items()))  # sort parts

# printed parts with category
for category in categories:
    if categories[category] == 'printed':

        #category_info
        cat_info = {}
        for part in in_csv:
            if in_csv[part]['type'] == 'category_info' and in_csv[part]['category'] == category:
                cat_info = in_csv[part]
                break
        write_part_to_csv('', {'type':'category_info'}, {'category': category,'price': cat_info.get('price',''),'note':cat_info.get('note','')}, writer)

        for part in parts:
            if parts[part]['type'] == 'printed' and part in in_csv and in_csv[part]['category'] == category:
                write_part_to_csv(part, parts[part], in_csv.get(part, {}), writer)

# printed parts without category
for part in parts:
    if parts[part]['type'] == 'printed':
        if part in in_csv and in_csv[part]['category'] != '': continue
        write_part_to_csv(part, parts[part], in_csv.get(part, {}), writer)


# empty row
#writer.writerow({})
# mechanical parts with category
for category in categories:
    if categories[category] == 'mechanical':

        #category_info
        cat_info = {}
        for part in in_csv:
            if in_csv[part]['type'] == 'category_info' and in_csv[part]['category'] == category:
                cat_info = in_csv[part]
                break
        write_part_to_csv('', {'type':'category_info'}, {'category': category,'price': cat_info.get('price',''),'note':cat_info.get('note','')}, writer)

        for part in parts:
            if parts[part]['type'] == 'mechanical' and part in in_csv and in_csv[part]['category'] == category:
                write_part_to_csv(part, parts[part], in_csv.get(part, {}), writer)

# mechanical parts without category
for part in parts:
    if parts[part]['type'] == 'mechanical':
        if part in in_csv and in_csv[part]['category'] != '': continue
        write_part_to_csv(part, parts[part], in_csv.get(part, {}), writer)

csvfile.close()