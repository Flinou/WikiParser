# -*- coding: utf-8 -*-
import lxml.etree

def sortDicoFile(output, outputSorted):
    with open(output, 'a+', 0) as dictionnary:
        dictionnary.write("</root>")
    def sortchildrenby(parent, attr):
        parent[:] = sorted(parent, key=lambda child: child.get(attr))

    parser = lxml.etree.XMLParser(strip_cdata=False)
    tree = lxml.etree.parse(output, parser)
    root = tree.getroot()

    sortchildrenby(root, 'val2')

    for c in root:
        sortchildrenby(c, 'desc')

    for c in root:
        c.attrib.pop("val2", None)

    with open(outputSorted, 'w', 0) as f:
        f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n" + lxml.etree.tostring(root, encoding="utf-8", method="xml"))

