print('-Creating README')

import csv

# read csv
csv_data = {}
try:
    with open('./Parts/bom.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            csv_data[row['cad_name']] = row
except:
    print('No bom.csv found!')

#create table strings
printed_table = ''
mechanical_table = ''
for row in csv_data:
    entry = csv_data[row]
    if entry['type'] == 'printed':
        printed_table += '| '+str(entry['cad_name'])+ ' | [STL](./Printed%20Parts/STL/'+str(entry['cad_name'])+'.stl) | [STEP](./Printed%20Parts/STEP/'+str(entry['cad_name'])+'.step) | '+str(entry['amount'])+' | '+str(entry['note'].split('[t:')[1].split(';w:')[0])+' | '+str(entry['note'].split('[t:')[1].split(';w:')[1].split(']')[0])+' |\n'
    elif entry['type'] == 'mechanical':
        mechanical_table += '| ['+str(entry['cad_name'])+'](./Mechanical%20Parts/'+str(entry['cad_name'])+'.stl) | ['+('link' if str(entry['link']) != '---' else ':small_red_triangle:')+']('+str(entry['link'])+') | ['+('link' if str(entry['alt_link']) != '---' else ':small_red_triangle:')+']('+str(entry['alt_link'])+') | '+str(entry['amount'])+' | '+str(entry['price'])+' | '+str(entry['note'])+' |\n'


#README update
lines = None
with open('./Parts/README.md', "r") as f:
    lines = f.readlines()

printed_line, mechanical_line = 0, 0
for i, line in enumerate(lines):
    if '## Printed Parts' in line:
        printed_line = i +3
    if '## Mechanical Parts' in line:
        mechanical_line = i +1

with open('./Parts/README.md', "w") as f:
    for i, line in enumerate(lines):
        if i < printed_line:
            f.write(line)
        else:
            for entry in printed_table:
                f.write(entry)
            break

    for i, line in enumerate(lines):
        if i > printed_line:
            if line[0] != '|' and i < mechanical_line:
                f.write(line)
            elif i >= mechanical_line:
                f.write(line)
            if i == mechanical_line+1:
                for entry in mechanical_table:
                    f.write(entry)
                break

    for i, line in enumerate(lines):
        if i > mechanical_line and line[0] != '|':
            f.write(line)