import re
import collections
import csv
print('-Creating README')


def pad_column(title: str, longest: int, factor=1.575):
    padding = ' ' * int(((longest-len(str(title)))) / 2 * factor)
    return padding + title + padding

def write_printed(part_data) -> str:
    stl = '[STL](./Printed%20Parts/STL/'+str(part_data['cad_name'])+'.stl)'
    step = '[STEP](./Printed%20Parts/STEP/'+str(part_data['cad_name'])+'.step)'
    time = str(part_data['note'].split('[t:')[1].split('|w:')[0])
    weight = str(part_data['note'].split('[t:')[1].split('|w:')[1].split(']')[0])

    return '| '+str(part_data['cad_name']) + ' | '+stl+' | '+step+' | '+str(part_data['amount'])+' | '+time+' | '+weight+' |\n'

def write_mechanical(part_data) -> str:
    # shorten urls
    note = str(part_data['note'])
    urls = re.findall(r'(https?://[^\s]+)', note)
    for url in list(set(urls)):
        note = note.replace(url, '[link]('+url+')')

    part_name = '['+str(part_data['cad_name'])+'](./Mechanical%20Parts/'+str(part_data['cad_name'])+'.stl)'
    link = ('[link]('+str(part_data['link'])+')') if str(part_data['link']) != '---' else ':small_red_triangle:'

    #add alt link to link
    if part_data['alt_link'] != '---':
        link += ' / [link]('+str(part_data['alt_link'])+')'

    return '| '+part_name+' | '+str(part_data['amount'])+' | '+link+' | '+str(part_data['price'])+' | '+str(note)+' |\n'


# read csv
csv_data = {}
try:
    with open('./Parts/bom.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            csv_data[row['cad_name']] = row
except:
    print('No bom.csv found!')

categories = {}

#gather max lengths for each column
column_lengths = {'printed': {}, 'mechanical': {}}
for part in csv_data:
    part_data = csv_data[part]

    #skip empty row
    if part_data['type'] in ['','category_info'] : continue

    for column in part_data.keys():

        #register all columns
        if column not in column_lengths[part_data['type']]:
            column_lengths[part_data['type']][column] = 0

        #skip '---'
        if part_data[column] == '---': continue

        column_length = len(str(part_data[column]))

        #detect url in note
        #if column == 'note':
        urls = re.findall(r'(https?://[^\s]+)', str(part_data[column])) #get all urls in note as list
        for url in urls: column_length = column_length - len(str(url)) + 4  #length of real url gets replaced with displayed 'link' message length
        
        #add alt_link length to link
        if column == 'link' and part_data['alt_link'] != '---':
            column_length += 7

        if column_lengths[part_data['type']][column] < column_length:
            column_lengths[part_data['type']][column] = column_length

    #add category if not exists {'category_name':'printed/mechanical'}
    if part_data['category'] not in categories and part_data['category'] != '':
        categories[part_data['category']] = part_data['type']

categories = collections.OrderedDict(
    sorted(categories.items()))  # sort cats


#create table strings
printed_table = ''
mechanical_table = ''

#create table header strings
printed_header = '|'+pad_column('Part Name', column_lengths['printed']['cad_name'], 2.4)+'| STL | STEP |'+pad_column('Amount', column_lengths['printed']['amount'])+'| Print Time | Weight (g)|\n| --- | --- | --- | --- | --- | --- |\n'
mechanical_header = '|'+pad_column('Part Name', column_lengths['mechanical']['cad_name'], 2.4)+'|'+pad_column('CAD Amount', column_lengths['mechanical']['amount'])+'| '+pad_column('Link', column_lengths['mechanical']['link'])+' |'+pad_column('Price', column_lengths['mechanical']['price'], 2)+'|'+pad_column('Note', column_lengths['mechanical']['note'])+'|\n| --- | --- | --- | --- | --- |\n'

#create category title + table header
for category in categories:
    if categories[category] == 'printed':
        printed_table += '\n### '+str(category).upper()+':\n' + printed_header
    if categories[category] == 'mechanical':
        mechanical_table += '\n### ' + \
            str(category).upper()+':\n' + mechanical_header


    #create table strings for parts with category
    for part in csv_data:
        part_data = csv_data[part]

        #skip if no category
        if part_data['category'] != category: continue

        if part_data['type'] == 'printed':
            printed_table += write_printed(part_data)

        elif part_data['type'] == 'mechanical':
            mechanical_table += write_mechanical(part_data)

# set header for parts without category
if 'printed' in categories.values():
    printed_table += '\n' + printed_header
else:
    printed_table = '\n' + printed_header
if 'mechanical' in categories.values():
    mechanical_table += '\n' + mechanical_header
else:
    mechanical_table = '\n' + mechanical_header

#create table strings for parts without category
for part in csv_data:
    part_data = csv_data[part]

    #skip if has category
    if part_data['category'] != '': continue

    if part_data['type'] == 'printed':
        printed_table += write_printed(part_data)

    elif part_data['type'] == 'mechanical':
        mechanical_table += write_mechanical(part_data)


# README update
lines = None
with open('./Parts/README.md', "r") as f:
    lines = f.readlines()

lines_iter = iter(lines)
with open('./Parts/README.md', "w") as f:

    line = next(lines_iter)

    # Fing begining of printed table
    while '##' not in line and 'Printed Parts' not in line:
        f.write(line)
        line = next(lines_iter)
    f.write(line)

    # write printed table
    for x in printed_table:
        f.write(x)

    # find end of table
    while line[:2] != '``':
        line = next(lines_iter)
    f.write('\n')

    # Fing begining of mechanical table
    while '##' not in line and 'Mechanical Parts' not in line:
        f.write(line)
        line = next(lines_iter)
    f.write(line)

    # write mechanical table
    for x in mechanical_table:
        f.write(x)

    # find end of table
    while line[:2] != '``':
        line = next(lines_iter)
    f.write('\n')

    while line:
        f.write(line)
        line = next(lines_iter, False)
