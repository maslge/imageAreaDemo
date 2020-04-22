#!/usr/bin/env python3

import csv
import datetime
import platform
import getpass

from jinja2 import Environment, FileSystemLoader
from os import listdir
from shutil import copyfile


# print(sys.version)
# les constantes
CURRENT_DATE_TIME = datetime.datetime.now()
CURRENT_DATE_STRING = CURRENT_DATE_TIME.strftime('%d/%m/%y %I:%M %S %p')
GENERATED_METADATA = CURRENT_DATE_STRING + ", " + platform.platform() + ", " + getpass.getuser()

# les templates sont dans le repertoire src
file_loader = FileSystemLoader('./src/')
env = Environment(loader=file_loader)
TEMPLATE_INDEX_HTML = env.get_template("templateIndex.html")
TEMPLATE_INTERACTIVE_IMAGE_CAPTION = env.get_template("templateCaptionFullCss.html")
TEMPLATE_INTERACTIVE_IMAGE_HTMLDOC = env.get_template("templateCaptionFullCssPageHTML.html")
DIRECTORY_SRC_For_CSV_PNG = "./Upload_CSV_and_PNG_HereToGenerateWebSite/"


def generateIndexHTML(indexMap):
    output = TEMPLATE_INDEX_HTML.render(indexMap=indexMap, generatedMetaData=GENERATED_METADATA)
    file = open("./webcontent/index.html", 'w')
    file.write(output)
    file.close()


def generateInteractiveImage(name):
    htmlInteractiveImage = ""
    output = ""
    with open(DIRECTORY_SRC_For_CSV_PNG + name + ".csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            # print(row[0],row[1],row[2], row[3], row[4] )
            if (line_count == 0):
                # premire ligne = les titre et le blabla du doc master et les dimensions de l'image
                text_title = row[0]
                text_body_intro = row[1]
                text_body_conclusion = row[2]
                imageWidth = row[3]
                imageHeight = row[4]
            else:
                # les autres lignes les datas pour les captions dans l'image
                output += TEMPLATE_INTERACTIVE_IMAGE_CAPTION.render(
                    posx=row[0], posy=row[1], title=row[2], body=row[3], footer=row[4])
            # print(output)
            line_count += 1
    # print('Processed ', line_count ,' lines.')
    # print(output)
    toolchainPNGFile = name + ".png"
    htmlInteractiveImage = TEMPLATE_INTERACTIVE_IMAGE_HTMLDOC.render(toolchainPNGFile=toolchainPNGFile, text_title=text_title, text_body_intro=text_body_intro,
                                                                     text_body_conclusion=text_body_conclusion, imageWidth=imageWidth, imageHeight=imageHeight, injectFullDivContentHere=output, generatedMetaData=GENERATED_METADATA)

    file = open("./webcontent/" + name + ".html", 'w')
    file.write(htmlInteractiveImage)
    file.close()
    copyfile(DIRECTORY_SRC_For_CSV_PNG + toolchainPNGFile, "./webcontent/" + toolchainPNGFile)
    # return the title of the html document to use it as the label for the link from the index.html page
    print ({name: text_title})
    return {name: text_title}


def generateFullWebSite():
    # Check compliance of the data source directory ... nbr of elements and PNG, CSV format, ...
    list = listdir(DIRECTORY_SRC_For_CSV_PNG)
    print ("contenu du repertoire source pour la generation : ")
    print (list)

    numberOfElements = len(list)
    print ("number of elements : ")
    print (numberOfElements)

    # Check that the number of files in directory CSV & PNG is pair sinon ALARLM !!!
    if (numberOfElements % 2 == 1):
        print("impair")
        print (list)
        raise ValueError(
            'Number of files in the directory CSV & PNG is not odd ! For each interactive image to generate you need to include One dataSet as CSV and the PNG corresponding in the directory')

    # Donc si on est là => pair => finalement j'ai 2 fois moins d'image interactiove à generer que de fichuier dans le repertoire
    numberOfInteractiveImages = int(numberOfElements / 2)
    listOfInteractiveImages = [None] * numberOfInteractiveImages

    # get FileName list from directory content
    # trie pour simplifier le traitement
    list.sort()

    # je prends un elements sur 2 pour consituer ma liste d'image à generer et on lance la generation
    for k in range(0, numberOfInteractiveImages):
        listOfInteractiveImages[k] = list[2*k][:-4]
        # check if that next element in the list have the same name ... otherwise trigger an ERROR ...
        if listOfInteractiveImages[k] != list[2*k+1][:-4]:
            raise ValueError(
                'For each interactive image to generate you need to include One dataSet as CSV File and the PNG corresponding withe the same namefile in the directory ')

    print("list of interactive images to generate : ")
    print(listOfInteractiveImages)

    listOfLinkLabelForIndex = [None] * numberOfInteractiveImages
    indexMap = {}
    # parcours la list pour lancer la generation de chaque image
    for intercativeImageItemName in listOfInteractiveImages:
        # print ("generate interactive HTML Page for : "+ intercativeImageItemName)
        indexMap.update(generateInteractiveImage(intercativeImageItemName))

    # Generate the index.html file for the website
    print ("generate index.html ")
    generateIndexHTML(indexMap)


generateFullWebSite()
