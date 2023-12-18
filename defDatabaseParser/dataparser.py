import xml.etree.ElementTree as ET
import sqlite3
import os
files_path = '../StudioProjects/Dico/app/src/test/resources/'
#files_path = './'

con = sqlite3.connect("definitions.db")
cur = con.cursor()
index = 1

for filename in os.listdir(files_path):
    print("file " + str(index))
    index = index + 1
    if filename.endswith(".xml"):
        tree = ET.parse(files_path + filename)
        root = tree.getroot()

        for child in root:
            syn=""
            wordAttribs=child.attrib
            word=wordAttribs.get('val')
            for types in child:
                if types.find('def') is not None:
                    definition=types.find('def').text
                if types.find('nature') is not None:
                    nature=types.find('nature').text
                if types.find('syn') is not None:
                    syn=types.find('syn').text
                cur.execute("INSERT INTO DEFINITIONS VALUES (NULL, ?, ?, ?, ?)", (nature, definition, syn, word))
                con.commit()

