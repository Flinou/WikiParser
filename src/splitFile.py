# -*- coding: utf-8 -*-

def splitDicoFile(output, lines_per_file):
    splitfile = None
    cpt = 1
    split_filename = output + str(cpt) + '.xml'
    splitfile = open(split_filename, "w")
    splitLimitReached = False
    with open(output) as outputFile:
        for lineno, line in enumerate(outputFile, 1):
            if lineno % lines_per_file == 0:
                splitLimitReached = True
            if splitLimitReached and "</definition>" in line:
                splitfile.write(line + "</root>\n")
                splitfile.close()
                cpt = cpt + 1
                split_filename = output + str(cpt) + '.xml'
                splitfile = open(split_filename, "w")
                splitfile.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n" + "<root>\n")
                splitLimitReached = False
                continue
            splitfile.write(line)
        if splitfile:
            splitfile.close()
