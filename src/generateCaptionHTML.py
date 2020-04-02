#!/usr/bin/env python3
import csv

from jinja2 import Environment, FileSystemLoader


file_loader = FileSystemLoader('./src/')
env = Environment(loader=file_loader)
template = env.get_template("templateCaption.html")


with open('./src/dataCaption.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    for row in csv_reader:
        #print(row[0],row[1],row[2], row[3], row[4] )
        output = template.render(posx=row[0], posy=row[1], title=row[2], body=row[3], footer=row[4])
        print(output)
        line_count += 1
    print('Processed ', line_count ,' lines.')
