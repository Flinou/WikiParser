# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 Bruno Coudoin
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, see <http://www.gnu.org/licenses/>.
#

#
# Implementation of the wiktionary model
# used

import os.path
import re
import unidecode

id = 0
firstWrite = True
# Represent the description of a definition
# This is recursive, a description can hold an
# unlimited number of subdescription
class Description:

    def __init__ (self, parent, text, level, numbered = False):
        global id
        self.id = id
        id += 1
        self.parent = parent
        self.level = level
        self.text = text
        self.numbered = numbered
        self.descriptions = []

    def isEmpty(self):
        if len(self.descriptions) > 0:
            return False
        return True

    # Return True if this node's text field of one of its
    # children is not empty
    def hasContent(self):
        if len(self.text) > 0:
            return True
        else:
            for d in self.descriptions:
                if d.hasContent():
                    return True
        return False

    # Recursively find the node at the given level
    def getNodeAtLevel(self, level):
        if level >= self.level:
            return self
        elif level < self.level:
            return self.parent.getNodeAtLevel(level)

    def addDescription(self, text, level, numbered):
        node = self.getNodeAtLevel(level - 1)
        if node:
            description = Description(node, text, level, numbered)
            node.descriptions.append( description )
            return description
        return None
    
    def isData(self, description):
        if len(description.text) < 1:
            return False
        else:
            return True

    def dump2html(self, f):
        global firstWrite
        if len(self.text) > 0 and not str(self.text).isspace() and self.text.strip():
            #For Android display purposes, need those tricks
            if "INS_NL_BEF" in self.text and firstWrite:
                self.text = re.sub("INS_NL_BEF","", self.text)
                f.write ( "<li>" + self.text + "</li><br><br>" )
            elif "INS_NL_BEF" in self.text and not firstWrite:
                self.text = re.sub("INS_NL_BEF","", self.text)
                f.write ( "\n<li>" + self.text + "</li><br><br>" )
            #elif "INS_NL_AFT" in self.text:
             #   self.text = re.sub("INS_NL_AFT","", self.text)
              #  f.write ( "<li>" + self.text + "</li>\n" )
            else:
                f.write ( "<li>" + self.text + "</li>" )
            firstWrite = False
        #self.Descriptions => exemple
 #       self.descriptions = filter(self.isData, self.descriptions)
        if len(self.descriptions) > 0:
#            self.descriptions[-1].text=self.descriptions[-1].text + "IS_LAST"
            for d in self.descriptions:
                d.dump2html(f)
            




class Definition:

    def __init__ (self):
        self.type = ""
        self.subType = ""
        self.filtered = False
        self.gender = ""
        self.rootDescription = Description(None, "", -1)
        self.currentDescription = self.rootDescription
        self.synonym = []
        self.antonym = []
        self.anagram = []
        self.hyperonym = []
        self.hyponym = []
        self.prononciation = []
        self.category = []
        self.image = []

    def setType(self, type):
        self.type = type

    def setSubType(self, subType):
        self.subType = subType

    def setGender(self, gender):
        self.gender = gender

    # A definition may hold several descriptions, each one can
    # have several sub descriptions.
    def addDescription(self, text, level, numbered):
        self.currentDescription = \
            self.currentDescription.addDescription(text, level, numbered)

    def add(self, atype, text):
        if len(text) == 0:
            return

        if atype == Wiktio.ANAGRAM:
            self.anagram.append(text)
        elif atype == Wiktio.SYNONYM:
            self.synonym.append(text)
        elif atype == Wiktio.ANTONYM:
            self.antonym.append(text)
        elif atype == Wiktio.HYPERONYM:
            self.hyperonym.append(text)
        elif atype == Wiktio.HYPONYM:
            self.hyponym.append(text)
        elif atype == Wiktio.PRON:
            self.prononciation.append(text)
        elif atype == Wiktio.IMAGE:
            self.image.append(text)
        elif atype == Wiktio.CATEGORY:
            self.category.append(text)
        else:
            print "!!ERROR!!: Type not supported"

    def dump2htmlImage(self, f):
        if self.image:
            prefix = "http://fr.wiktionary.org/wiki/Fichier:"
            for img in self.image:
                f.write ( "<a href='" + prefix + img + "'>" + \
                    img + '</a><br/>' )

    def dump2html(self, f, name):
        global firstWrite
        if self.filtered or not self.rootDescription.hasContent():
            return
        name = str(name).lower()
        unaccentedName = unidecode.unidecode(unicode(name,"utf-8"))
        f.write ( "\t<definition val=\"" + name + "\"" + " val2=\"" + unaccentedName + "\">\n" )
        f.write ("\t\t<nature><![CDATA[<i><b>" + self.type + " " + self.gender + "</i></b>]]></nature>\n")
        f.write("\t\t<def><![CDATA[")
        #self.dump2htmlImage(f)
        self.rootDescription.dump2html(f)
        firstWrite = True
        f.write("]]></def>\n")
        f.write ( "\t</definition>\n" )

class Word:

    def __init__ (self, name = None):
        self.name = name
        self.definition = []

    def setName(self, name):
        self.name = name

    def addDefinition(self, definition):
        self.definition.append(definition)

    def dump2html(self, f):
        if not self.definition:
            f.write ( "<h2>ERROR: NO DEFINITION</h2>" )
            return
        for d in self.definition:
            d.dump2html(f, self.name)


class Wiktio:

    (DEFINITION,
     ANAGRAM,
     SYNONYM,
     ANTONYM,
     HYPERONYM,
     HYPONYM,
     PRON,
     IMAGE,
     CATEGORY,
     SKIP) = range(0, 10)

    def __init__ (self):
        self.words = []

    def addWord(self, word):
        self.words.append(word)

    def getWords(self):
        return self.words

    def sort(self):
        self.words.sort(key=lambda word: word.name.lower())

    def dumpHtmlHeader(self, f):
        with open(f, 'a+', 0) as f:
            f.write ( """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<root>
""")

    def dumpHtmlFooter(self, f):
        with open(f, 'a+', 0) as f:
            f.write ("""
</root>
""")

    # Creates a big HTML file, useful to debug
    def dump2html(self, file):
        with open(file, 'a+', 0) as f:
        #    self.dumpHtmlHeader(f)
            self.sort()
            for w in self.words:
                w.dump2html(f)
           # self.dumpHtmlFooter(f)

    # Creates a static HTML site in the given directory
''' def dump2htmlSite(self, baseDir):
        if not os.path.isdir(baseDir):
            print "ERROR: Directory '" + baseDir + "' does not exists."
            return

        letter = "/"
        self.sort()
        with open(baseDir + '/index.html', 'w') as f_index:
            self.dumpHtmlHeader(f_index)
            for w in self.words:
                if letter[0] != w.name[0].upper():
                    letter = w.name[0].upper()
                    f_index.write ( "<hr/><h1>" + letter[0] + "</h1>" )
                f_index.write ( "<a href='" + w.name + ".html'>" + w.name + "</a> " )
                with open(baseDir + '/' + w.name + '.html', 'w') as f:
                    self.dumpHtmlHeader(f)
                    w.dump2html(f)
                    self.dumpHtmlFooter(f)

            self.dumpHtmlFooter(f_index)
'''
