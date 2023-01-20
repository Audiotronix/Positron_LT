import csv

# read csv
csv_data = {}
try:
    with open('./Parts/bom.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            if row['type'] != 'printed': continue
            support = row['note'].split('|s:')[1].split('|')[0]
            csv_data[row['cad_name']] = {'support': support}
except:
    print('No bom.csv found!')

lines = None
with open('./Parts/Printed Parts/README.md', "r") as f:
    lines = f.readlines()

table_header = '| Part Name | Orientation | Supports | Inserts |\n| :---: | --- | --- | --- |\n'

lines_iter = iter(lines)
with open('./Parts/Printed Parts/README.md', "w") as f:

    line = next(lines_iter)

    # Find begining of table
    while '## Printing' not in line:
        f.write(line)
        line = next(lines_iter)
    f.write(line)

    f.write(table_header)

    for part in csv_data:
        stl_link = '[' +str(part)+ '](./STL/' +str(part)+'.stl)'
        sliced_link = '"../../Gallery/Sliced/'+str(part)+'.png"'
        sliced_img = '<img src='+sliced_link+' width="300">'
        preped_link = '"../../Gallery/Preped/'+str(part)+'.jpg"'
        preped_img = '<img src='+preped_link+' width="300">'
        f.write('|'+stl_link+' | '+sliced_img+' | '+ str(csv_data[part]['support']) +' | '+preped_img+'|\n')

    # find end of table
    while 'table_end' not in line:
        line = next(lines_iter)
    #f.write(line)
    #f.write("<div name='table_end'/>\n")

    # write remaining
    while line:
        f.write(line)
        line = next(lines_iter, False)