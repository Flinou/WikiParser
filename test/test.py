# -*- coding: utf-8 -*-
import re
import lxml.etree 
import os
def sortchildrenby(parent, attr):
    parent[:] = sorted(parent, key=lambda child: child.get(attr))

with open('dico', 'r') as myfile:
  data = myfile.read()

parser = lxml.etree.XMLParser(strip_cdata=False)
tree = lxml.etree.parse('dico', parser)

root = tree.getroot()

sortchildrenby(root, 'val')
for c in root:
    c[:] =  sorted(c, key=lambda child: (child.get('desc')))


with open('testsorted', 'a+', 0) as file:
  file.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n")
  file.write(lxml.etree.tostring(root,encoding="utf-8", method="xml"))


lines_per_file = 50000
smallfile = None
cpt = 1
small_filename = 'dico' + str(cpt) + '.xml'
smallfile = open(small_filename, "w")
splitLimitReached = False
with open('dico') as bigfile:
    for lineno, line in enumerate(bigfile, 1):
        if lineno % lines_per_file == 0:
            splitLimitReached = True
        if splitLimitReached and "</definition>" in line:
            smallfile.write(line + "</root>\n")
            smallfile.close()
            cpt = cpt + 1
            small_filename = 'dico' + str(cpt) + '.xml'
            smallfile = open(small_filename, "w")
            smallfile.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n" + "<root>\n")
            splitLimitReached = False
        smallfile.write(line)
    if smallfile:
        smallfile.close()


