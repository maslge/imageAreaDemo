#!/usr/bin/env python3
import csv, datetime, platform

from jinja2 import Environment, FileSystemLoader


file_loader = FileSystemLoader('./src/')
env = Environment(loader=file_loader)
template = env.get_template("templateCaptionFullCss.html")
output=""

with open('./src/dataCaption.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        #print(row[0],row[1],row[2], row[3], row[4] )
        output += template.render(posx=row[0], posy=row[1], title=row[2], body=row[3], footer=row[4])
        #print(output)
        line_count += 1
    print('Processed ', line_count ,' lines.')
    #print(output)

template = env.get_template("templateCaptionFullCssPageHTML.html")
current_date_time = datetime.datetime.now()
dt_string = current_date_time.strftime('%d/%m/%y %I:%M %S %p')
info = dt_string + " / " + platform.platform()
FinalHTMLDocument = template.render(injectFullDivContentHere=output, genTime=info)
#print(FinalHTMLDocument)

file = open('FinalHTMLDoc.html', 'w')
file.write(FinalHTMLDocument)
file.close()
