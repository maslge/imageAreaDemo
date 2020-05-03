#!/usr/bin/python3
import datetime
import getpass
import json
import platform
import os
import csv

from jinja2 import Environment, FileSystemLoader, Template
from pykson import Pykson, JsonObject, StringField, ObjectListField, ObjectField
from os import listdir
from shutil import copyfile




# print(sys.version)
# les constantes
CURRENT_DATE_TIME = datetime.datetime.now()
CURRENT_DATE_STRING = CURRENT_DATE_TIME.strftime('%d/%m/%y %I:%M %S %p')
GENERATED_METADATA = CURRENT_DATE_STRING + ", " + platform.platform() + ", " + getpass.getuser()

# les templates sont dans le repertoire src
file_loader = FileSystemLoader('./')
env = Environment(loader=file_loader)
TEMPLATE_INDEX_HTML = env.get_template("templateIndex.html")
TEMPLATE_INTERACTIVE_IMAGE_CAPTION = env.get_template("templateCaptionFullCss.html")
TEMPLATE_INTERACTIVE_IMAGE_HTMLDOC = env.get_template("templateCaptionFullCssPageHTML.html")
DIRECTORY_OF_SRC_CONFIG_TO_GENERATE_WEBSITE = "./Upload_Here_Config_To_Generate_WebSite/"
DIRECTORY_WEBCONTENT = "./webContent/"

class Picture:
    """
        blalblalbla
    """
    file : str
    width : str
    height : str

    def __init__(self, file, width, height):
        self.file = file
        self.width = width
        self.height = height


class Popup:
    headerText : str
    bodyHtml : str
    footerText : str

    def __init__(self, headerText, bodyHtml, footerText):
        self.headerText = headerText
        self.bodyHtml = bodyHtml
        self.footerText = footerText


class Caption:
    posx : str
    posy :str
    popup : Popup

    def __init__(self, posx : str, posy : str, headerText :str, bodyHtml : str, footerText : str):
        self.posx = posx
        self.posy = posy
        self.popup = Popup(headerText, bodyHtml, footerText)

    def renderHTML(self) -> str :
        print(self.posx, self.posy)
        return TEMPLATE_INTERACTIVE_IMAGE_CAPTION.render(posx=self.posx, posy=self.posy, title=self.popup.headerText, body=self.popup.bodyHtml, footer=self.popup.footerText)

class InteractiveImage:
    """
        final object that carry all the data for the generation and also the operation for generating the final interactive image
    """
    title : str
    headerHtml : str
    footerHtml :str
    picture : Picture
    captions : list # list of captions

    # parameterized constructor
    def __init__(self,title : str, headerHtml : str, footerHtml : str, picture : Picture, captions : list):
        self.title = title
        self.headerHtml = headerHtml
        self.footerHtml = footerHtml
        self.picture = picture
        self.captions = captions

    def __renderHtmlForCaptions__(self) -> str:
        captionsContent = ""
        for caption in self.captions:
            captionsContent += caption.renderHTML()
        return captionsContent

    def renderHtmlContentWithTemplates(self) -> str:
        c = self.__renderHtmlForCaptions__()
        return TEMPLATE_INTERACTIVE_IMAGE_HTMLDOC.render(toolchainPNGFile=self.picture.file, text_title=self.title, text_body_intro=self.headerHtml, text_body_conclusion=self.footerHtml, imageWidth=self.picture.width, imageHeight=self.picture.height, injectFullDivContentHere= c, generatedMetaData=GENERATED_METADATA)



class PictureReaderForJSON(JsonObject):
    """
        blalblalbla
    """
    file = StringField()
    width = StringField()
    height = StringField()

    def export(self) -> Picture :
        return Picture(self.file, self.width, self.height)

class PopupReaderForJSON(JsonObject):
    headerText = StringField()
    bodyhtml = StringField()
    footertext = StringField()

    def export(self) -> Popup :
        return Popup(self.headerText, self.bodyhtml, self.footertext)


class CaptionReaderForJSON(JsonObject):
    posx = StringField()
    posy = StringField()
    popup = ObjectField(PopupReaderForJSON)

    def export(self) -> Caption :
        return Caption(self.posx, self.posx, self.popup.headerText, self.popup.bodyhtml, self.popup.footertext)

class InteractiveImagesReaderForJSON(JsonObject):
    """
        pykson class for deserialization from json file format
    """
    name = StringField()
    headerhtml = StringField()
    footerhtml = StringField()
    picture = ObjectField(PictureReaderForJSON)
    captions = ObjectListField(CaptionReaderForJSON)

    def __export__(self) -> InteractiveImage:
        caption2R = []
        for c in self.captions:
            caption2R.append(c.export())
        return InteractiveImage(self.name, self.headerhtml, self.footerhtml, self.picture.export(), caption2R)


    def __readConfigAndGenerateInteractiveImagesReaderFromJSON__(filename : str):
        with open(filename, "r") as toolchainDataJson_file:
            json_doc = json.load(toolchainDataJson_file)
        print(json_doc)
        t = Pykson().from_json(json_doc, InteractiveImagesReaderForJSON)
        return t

    def generateInteractiveImagesFromJSONConfFile(filename : str) -> InteractiveImage :
        toolchain = InteractiveImagesReaderForJSON.__readConfigAndGenerateInteractiveImagesReaderFromJSON__(DIRECTORY_OF_SRC_CONFIG_TO_GENERATE_WEBSITE + f)
        return toolchain.__export__()



class InteractiveImagesReaderForCSV():
    """
        Todo blabla
    """

    def generateInteractiveImagesFromCSVConfFile(filename : str): #todo revoir filename : str ... pourquoi pas file directement !!!!
        captions = list()
        picture : Picture
        title : str
        body_intro :str
        body_conclusion : str
        with open(filename, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                print(row)
                if (line_count == 0):
                    title = row[0]
                    body_intro = row[1]
                    body_conclusion = row[2]
                    picture = Picture(row[3], row[4], row[5])
                captions.append(Caption(row[6], row[7], row[8], row[9], row[10]))
                line_count += 1
        return InteractiveImage(title, body_intro, body_conclusion, picture, captions)



interactiveImagesMap = {}

# lecture et analyse de la conf
files = listdir(DIRECTORY_OF_SRC_CONFIG_TO_GENERATE_WEBSITE)
print ("contenu du repertoire source pour la generation : ")
print (files)

for f in files :
# deserialize from the source file
    """
        Parcourir la liste des fichiers de conf, les lit et generate les interactiveimage assosciées
    """
    if f.endswith(".json"):

        interactiveImageID = os.path.splitext(f)[0]
        interactiveImage = InteractiveImagesReaderForJSON.generateInteractiveImagesFromJSONConfFile(DIRECTORY_OF_SRC_CONFIG_TO_GENERATE_WEBSITE + f)
        interactiveImagesMap[interactiveImageID] = interactiveImage

    elif f.endswith(".CSV"):

        interactiveImageID = os.path.splitext(f)[0]
        interactiveImage = InteractiveImagesReaderForCSV.generateInteractiveImagesFromCSVConfFile(DIRECTORY_OF_SRC_CONFIG_TO_GENERATE_WEBSITE + f)
        interactiveImagesMap[interactiveImageID] = interactiveImage

    elif f.endswith(".xml"):
        print("xml not currently implemented")
        raise Exception
    elif f.endswith(".yaml"):
        print("xml not currently implemented")
        raise Exception

# generation du site
indexMap = {} #name=interactiveImageID, title=interactiveImage.
for interactiveImageID, interactiveImage in interactiveImagesMap.items():
    file = open(DIRECTORY_WEBCONTENT + interactiveImageID + ".html", 'w')
    file.write(interactiveImage.renderHtmlContentWithTemplates())
    file.close()
    copyfile(DIRECTORY_OF_SRC_CONFIG_TO_GENERATE_WEBSITE + interactiveImage.picture.file, DIRECTORY_WEBCONTENT + interactiveImage.picture.file)
    indexMap[interactiveImageID] = interactiveImage.title

output = TEMPLATE_INDEX_HTML.render(indexMap=indexMap, generatedMetaData=GENERATED_METADATA)
file = open(DIRECTORY_WEBCONTENT + "index.html", 'w')
file.write(output)
file.close()


