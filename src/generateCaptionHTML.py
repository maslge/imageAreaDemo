#!/usr/bin/env python3
import csv, datetime, platform, getpass
import sys


from jinja2 import Environment, FileSystemLoader

print(sys.version)

file_loader = FileSystemLoader('./src/')
env = Environment(loader=file_loader)
template = env.get_template("templateCaptionFullCss.html")
output=""

with open('./src/dataCaption.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        #print(row[0],row[1],row[2], row[3], row[4] )
        if (line_count == 0 ):
            # premire ligne = les titre et le blabla du doc master
            text_title=posx=row[0]
            text_body_intro=row[1]
            text_body_conclusion=row[2]
        else:
            # les autres lignes les datas pour les captions dans l'image
            output += template.render(posx=row[0], posy=row[1], title=row[2], body=row[3], footer=row[4])
        #print(output)
        line_count += 1
    print('Processed ', line_count ,' lines.')
    #print(output)

template = env.get_template("templateCaptionFullCssPageHTML.html")
current_date_time = datetime.datetime.now()
dt_string = current_date_time.strftime('%d/%m/%y %I:%M %S %p')
info = dt_string + ", " + platform.platform() + ", " + getpass.getuser()


FinalHTMLDocument = template.render(text_title=text_title, text_body_intro=text_body_intro, text_body_conclusion=text_body_conclusion, injectFullDivContentHere=output, generatedMetaData=info)
print(FinalHTMLDocument)

file = open('./webcontent/FinalHTMLDoc.html', 'w')
file.write(FinalHTMLDocument)
file.close()
