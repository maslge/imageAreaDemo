#!/usr/bin/env python3

import csv, datetime, platform, getpass
import sys
from jinja2 import Environment, FileSystemLoader
from os import listdir
from shutil import copyfile


#print(sys.version)
# les constantes
current_date_time = datetime.datetime.now()
dt_string = current_date_time.strftime('%d/%m/%y %I:%M %S %p')
generatedMetaData = dt_string + ", " + platform.platform() + ", " + getpass.getuser()
# les templates sont dans le repertoire src
file_loader = FileSystemLoader('./src/')
env = Environment(loader=file_loader)
templateIndexHTML = env.get_template("templateIndex.html")
templateInteractiveImage_Caption = env.get_template("templateCaptionFullCss.html")
templateInteractiveImage_HTMLDoc = env.get_template("templateCaptionFullCssPageHTML.html")
DirectorySourceFor_CSV_PNG = "./Upload_CSV_and_PNG_HereToGenerateWebSite/"

def generateIndexHTML (tableOfIndex) :
    output = templateIndexHTML.render(toolchainsList=tableOfIndex, generatedMetaData=generatedMetaData)
    file = open("./webcontent/index.html", 'w')
    file.write(output)
    file.close()

def generateInteractiveImage(name):
    htmlInteractiveImage=""
    output=""
    with open(DirectorySourceFor_CSV_PNG + name + ".csv") as csv_file:
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
                output += templateInteractiveImage_Caption.render(posx=row[0], posy=row[1], title=row[2], body=row[3], footer=row[4])
            #print(output)
            line_count += 1
    #print('Processed ', line_count ,' lines.')
    #print(output)
    toolchainPNGFile = name + ".png"
    htmlInteractiveImage = templateInteractiveImage_HTMLDoc.render(toolchainPNGFile=toolchainPNGFile, text_title=text_title, text_body_intro=text_body_intro, text_body_conclusion=text_body_conclusion, injectFullDivContentHere=output, generatedMetaData=generatedMetaData)

    file = open("./webcontent/" + name + ".html", 'w')
    file.write(htmlInteractiveImage)
    file.close()
    copyfile(DirectorySourceFor_CSV_PNG + toolchainPNGFile, "./webcontent/" + toolchainPNGFile)


def generateFullWebSite () :
    list = listdir(DirectorySourceFor_CSV_PNG)
    print ("contenu du repertoire source pour la generation : ")
    print (list)

    numberOfElements = len(list)
    print ("number of elements : ")
    print (numberOfElements) #Checks for the length of the list

    # check that the number of files in directory CSV & PNG is pair sinon ALARLM !!!
    if (numberOfElements % 2 == 1) :
        print("impair");
        print (list) #Outputs the whole list
        raise ValueError('Number of files in the directory CSV & PNG is not odd ! For each interactive image to generate you need to include One dataSet as CSV and the PNG corresponding in the directory ');


    # Donc si on est là => pair => finalement j'ai 2 fois moins d'image interactiove à generer que de fichuier dans le repertoire
    numberOfInteractiveImages = int(numberOfElements / 2);
    listOfInteractiveImages = [None] * numberOfInteractiveImages;

    # get FileName list from directory content
    # trie pour simplifier le traitement
    list.sort();

    # je prends un elements sur 2 pour consituer ma liste d'image à generer et on lance la generation
    for k in range(0, numberOfInteractiveImages):
        listOfInteractiveImages[k] = list[2*k][:-4];
        # check if that next element in the list have the same name ... otherwise trigger an ERROR ...
        if listOfInteractiveImages[k] != list[2*k+1][:-4]:
            raise ValueError('For each interactive image to generate you need to include One dataSet as CSV File and the PNG corresponding withe the same namefile in the directory ');

    print("list of interactive images to generate : ")
    print(listOfInteractiveImages);

    #generateMenu
    print ("generate index.html ")
    generateIndexHTML(listOfInteractiveImages)

    # parcours la list pour lancer la generation de chaque image
    for intercativeImageItemName in listOfInteractiveImages:
        #print ("generate interactive HTML Page for : "+ intercativeImageItemName)
        generateInteractiveImage(intercativeImageItemName)
    return;


generateFullWebSite();
