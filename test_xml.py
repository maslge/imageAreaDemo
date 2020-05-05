#!/usr/bin/python3

import xml.etree.ElementTree as ET

tree = ET.parse('./exampleConf/toolchainA.xml')
root = tree.getroot()
print(root)
print(len(list(root.getchildren())))

for child in root:
        print(child.tag)

print(root[0].tag) #name
print(root[1].tag)

#caption
print(root[4].attrib['posx'])
print(root[4].attrib['posy'])

print("-----------------")

print(root.find("headerhtml").text)
print(root.find("footerhtml").text)

for captionElement in root.findall("caption"):
    print (captionElement.attrib['posx'])
    print(captionElement.attrib['posy'])
    print(captionElement[0][0].text)
    print(captionElement[0][1].text)
    print(captionElement[0][2].text)


print(root.find('picture').attrib['file'])
