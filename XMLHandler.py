import xml.etree.ElementTree as ET
import xml.dom.minidom
import os


def deleteTags(root,ignore):
    if root.tag in ignore or str(root.text).strip() == '' :
        root.text = ''
    else:
         return
    for elem in root.getchildren():
        deleteTags(elem,ignore)

    return ET.ElementTree(root)


def format_xml(xmlString,ignoreArray):
    splitXML = xmlString.partition(">")
    xmlString = splitXML[0] + splitXML[1] + " " + splitXML[2]
    prettyxml = xml.dom.minidom.parseString(xmlString).toprettyxml()
    root = ET.fromstring(prettyxml)
    cleanXML = deleteTags(root,ignoreArray)
    cleanXML.write("xmlFile")
    openFile = xml.dom.minidom.parseString(open('xmlFile', 'r').read()).toprettyxml()
    os.remove('xmlFile')
    return str(openFile)

