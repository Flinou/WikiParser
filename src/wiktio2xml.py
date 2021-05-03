#!/usr/bin/python
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

from xml.sax import parse
from xml.sax.handler import ContentHandler
from wikimodele import *
from wikimodelearray import *
import sys
import re
import os
import lxml.etree

from optparse import OptionParser

import wiktio
import timeit
from wiktio import Wiktio
from splitFile import splitDicoFile
from sortFile import sortDicoFile
import importlib

compteur = 0
cpt = 0
debug = False
toAdd = False
# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass

class EndOfParsing(Error):
    """Raised when parsing is over"""
    pass

class WikiHandler(ContentHandler):
    

    def __init__ (self, searchWords, locale, _wiktio, output):
 
        self.searchWords= searchWords;
        self.output = output
        self.origin = output
        self.locale = locale
        self.wiktio = _wiktio
        self.cpt = 0

        self.isPageElement = False

        self.isTitleElement = False
        self.titleContent = ""

        self.isTextElement = False
        self.textContent = ""
        self.previousLineExample = False

        self.lilevel = 0
        self.wiktio.dumpHtmlHeader(self.output)

    def startElement(self, name, attrs):
        if name == 'page':
            self.isPageElement = True
        elif name == 'title':
            self.isTitleElement = True
            self.titleContent = ""
        elif name == 'text':
            self.isTextElement = True
            self.textContent = ""
        else:
            return

        self.genders = {
            "{{m}}": "masculin",
            "{{f}}": "féminin",
            "{{mf}}": "masculin et féminin"
            }

    def endElement(self, name):
        global compteur
        global cpt
        compteur = compteur + 1 
        if compteur % 10000 == 0:
            print("Element " + str(compteur) + " / 6600000")
        if name == 'page':
            self.isPageElement= False
            #make self.titleContent a plain string for accent comparison (accented word are not found in set if not used)
            self.titleContent = str(self.titleContent)
            if self.titleContent in self.searchWords:
                self.searchWords.remove(self.titleContent)
                word = self.parseText()
                matching_titleContent_whitespace = "Notadded"
                matching_titleContent_number = "Notadded" 
                if word and word.name:
                    #Remove words with space (expression for example). Keep words with accent thanks to re.UNICODE trick
                    matching_titleContent_whitespace = re.match(".* .*",self.titleContent, re.UNICODE)
                    #Remove words with digit in it
                    matching_titleContent_number = re.match("\d",self.titleContent)
                if len(self.titleContent) > 1 and matching_titleContent_whitespace is None and matching_titleContent_number is None and toAdd == True:
                    self.wiktio.addWord(word)
                    self.wiktio.dump2html(self.output)
                    self.wiktio = wiktio.Wiktio()
                cpt = cpt + 1 
                if cpt == 10000:
                    raise EndOfParsing
            self.titleContent = ""
            self.textContent = ""
        elif name == 'title':
            self.isTitleElement= False
        elif name == 'text':
            self.isTextElement = False
    def characters (self, ch):
        if self.isTitleElement:
            self.titleContent += ch
        elif self.isTextElement:
            self.textContent += ch


# Returns a list [text, level, numbered]
#
    def indents2xml(self, text, asText):
        numbered = False
        result = re.search(r"^[ ]*[*#:;]+[ ]*", text)
        if not result:
            self.lilevel = 0
            return [text, self.lilevel, numbered]

        indent = result.group(0).rstrip()
        self.lilevel = len(indent)
        text = text[result.end():]

        if asText:
            return [text, self.lilevel, numbered]

        if indent[-1:] == "#":
            numbered = True

        return [text, self.lilevel, numbered]

    # Replaces '''xx''' and ''xx'' from the given text
    # with openXml xx closeXml
    def quote2xml(self, quote, openXml, closeXml, text):
        index = 0
        while index >= 0:
            index = text.find(quote)
            index2 = text.find(quote, index + len(quote))
            if index >= 0 and index2 >=0:
                text = text.replace(quote, openXml, 1)
                text = text.replace(quote, closeXml, 1)
            else:
                return text
        return text

    # Replace standard Wiki tags to XML
    # Returns a list [text, level, numbered]
    # numbered = True if this is a numbered list
    def wiki2xml(self, text, asText, state):
        #Remove {{-}}, {{(}} and {{)}}
        text = re.sub(r"{{[-\)\(]}}", "", text)
        #Remove pattern like {{word:word}}
        text = re.sub(r"\[\[\w+:\w+\]\]", "", text)
        #Remove ref markup 
        text = re.sub(r"<ref>[\w\W]*</ref>", "", text)
        #text = re.sub(r"{{\(\|(.*)}}", r"", text)
        if text == "":
            return self.indents2xml(text, asText)

        [text, level, numbered] = self.indents2xml(text, asText)
        text = re.sub(r"{{w\|([^}]+)}}", r"<i>\1</i>", text)

        isComment = re.match("^''[^']", text) or re.match("^'''''[^']", text) or re.match("^{{[\W\w]*}}''[^']",text)
        

        if text.startswith("{{"):

            #Find all patterns like : {{some text}} in line
            matchings = re.findall(r"{{[\w\W]+?}}", text)
            for match in matchings:
                #Check if pattern is like {{text| or {{text}} and if so, save text (which is a precision for definition) 
                precision = re.match("{{([\w\W]+?)(\||}})", match)
                if precision and precision.group(1):
                    precisionVal = precision.group(1)
                    #check if the precision is worth adding in definition
                    if precisionVal in list(precisionsAllowed.keys()):
                        text = text.replace(match,precisionsAllowed[precisionVal]) 
        # Remove all unrecognized wiki tags
        #text = re.sub(r"{{[^}]+}}", "", text)
        text = re.sub(r"{{[\w\W]*}}$", "", text)
        varianteOrtho = re.match(r"{{variante ortho de\|([\w\W]+?)}}", text)
        if varianteOrtho and varianteOrtho.group(1):
            text = "Variante orthographique du mot " + varianteOrtho.group(1) +"."
        else:
            text = re.sub(r"{{[^}]+}}", "", text)

        # bold
        text = self.quote2xml("'''", "<b>", "</b>", text)
        # italic
        text = self.quote2xml("''", "<i>", "</i>", text)
        
        
        #Get rid of Image
        lowerText = text.lower()
        if lowerText.startswith("[[image") or lowerText.startswith("[[fichier") or lowerText.startswith("=") or lowerText.startswith("[[file"):
            text=""
            return [text, level, numbered]
        
        # Get rid of hyperlinks
        while text.find("[[") != -1:
            start = text.find("[[")
            stop = text.find("]]")
            pipe = text.find("|", start, stop)
            if pipe == -1:
                text = text.replace("[[", "", 1)
                text = text.replace("]]", "", 1)
            else:
                text = text[:start] + text[pipe+1:]
                text = text.replace("]]", "", 1)
        
        if state == Wiktio.SYNONYME:
            return [text,level, numbered]
        if isComment and self.previousLineExample:
            text=""
            self.previousLineExample=True
        elif isComment and len(text)>0:
            self.previousLineExample=True
        elif len(text) == 0 or str(text).isspace():
            self.previousLineExample = False
        else:
            text = text + "INS_NL_BEF"
            self.previousLineExample = False

        return [text, level, numbered]


    def checkFrenchSection(self, line, isFrenchSection):
        matchingLangSection = re.match(r"==( ?){{langue\|(.*)}}( ?)==",line,re.UNICODE)
        if matchingLangSection:
            if matchingLangSection.group(2) == "fr":
                return True
            else:
                return False
        else:
            return isFrenchSection 

    def synonymStringCreation(self, synonym, title, firstTitle):
        if firstTitle:
            synonym += title + " "
        else:
            synonym = re.sub(r', $','',synonym) 
            synonym += "<br>" + title + " "
        return synonym

    
    def handleSynonyms(self,text):
        synonym = ""
        firstTitle = True
        for line in text.splitlines():
            #Title are informations about register for use of synonyms 
            #Titles in synonyms section can be like '''Militaire''' or ; '''Militaire :'''
            matchingTitle = re.match(r";{0,1} *'{2,3}(.*?)\W{0,1}\:{0,1}'{2,3}", line, re.UNICODE)
            #Other title in synonym are like {{|Appareil portatif}}
            matchingOtherTitle = re.match(r"{{\|(.*)}}", line, re.UNICODE)
            if matchingTitle and not line.startswith("*"):
                title = "(" + matchingTitle.group(1) +")"
                synonym = self.synonymStringCreation(synonym, title, firstTitle)
                firstTitle = False
            elif matchingOtherTitle and not line.startswith("*"):
                title = "(" + matchingOtherTitle.group(1) +")"
                synonym = self.synonymStringCreation(synonym, title, firstTitle)
                firstTitle = False

            if line.startswith("*"):
                currentSyn = re.match(r".* \[\[(.*)\]\]", line, re.UNICODE)
                if currentSyn:
                    synonym += currentSyn.group(1) + ", "

        synonym = re.sub(r', $','',synonym) 
        return synonym



    # Wikipedia text content is interpreted and transformed in XML
    def parseText(self):
        value = 0
       # print "Processing " + self.titleContent
        inWord = wiktio.Word()
        frenchSection = False
        global toAdd
        toAdd = False
        state = Wiktio.SKIP

        wordType = ""
        wordSubType = ""
        filterIndent = ""
        gender = ""
        self.textContent=re.sub("(={2,} {)","PATTERN_TO_SPLIT_BY" + r"\1",self.textContent)
        #testSub = self.textContent
        #testSub=re.sub("(={3,} {)","PATTERN_TO_SPLIT_BY" + r"\1",testSub)
        #for textSplitted in re.split(r"(=== {{S\|.*\|fr\|{0,1}[\w\W]*?}} ===[\w\W]*?)=== {{S", self.textContent, flags=re.M|re.UNICODE):
        global currentDefinition
        for textSplitted in re.split(r"PATTERN_TO_SPLIT_BY", self.textContent, flags=re.M|re.UNICODE):
            firstLine = True

            # Append an end of text marker, it forces the end of the definition
            textSplitted += "\n{{-EndOfTest-}}"

            # Remove html comment (multilines)
            textSplitted = re.sub(r"<!--[^>]*-->", "",textSplitted, re.M)
            definition = wiktio.Definition()
            inWord.addDefinition(definition)
            concat = ""
            for l in textSplitted.splitlines():
                #Check if in French part of definition, if not break
                frenchSection = self.checkFrenchSection(l, frenchSection)
                if not frenchSection:
                    break
                startWithHash = False
                if l.startswith("#"):
                    startWithHash = True
                l = concat + l
                concat = ""
                next = False

                #Regarder le mot taf dans le wiktionnaire pour comprendre
                if re.search(r"<[^>]+$", l):
                    # Wiki uses a trick to format text area by ending in uncomplete
                    # html tags. In this case, we concat this line with the next one
                    # before processing it
                    concat = l
                    continue
                #Retrieve nature of the word in line like === {{S|wordNature|fr(|.*optional)}} ===
                matching_word_nature = re.match(r"=== {{S\|([\w\W]*?)\|fr}} ===",l,re.UNICODE)
                matching_word_nature_bis = re.match(r"=== {{S\|([\w\W]*?)\|fr\|.*}} ===",l,re.UNICODE)
                matching_word_nature_bis = re.match(r"=== {{S\|([\w\W]*?)\|fr\|.*}} ===",l,re.UNICODE)
                matching_synonyme = re.match(r"==== {{S\|synonymes}} ====",l,re.UNICODE)

                # Determine the section of the document we are in
                
                if firstLine and not matching_word_nature and not matching_word_nature_bis and not matching_synonyme:
                    break

                if matching_word_nature or matching_word_nature_bis:
                    currentDefinition = definition
                elif matching_synonyme:
                    definition = currentDefinition
                firstLine = False
                    
                if l.startswith("'''" + self.titleContent + "'''") or l.startswith("'''" + self.titleContent + " '''"):
                    for wt in list(self.genders.keys()):
                        if re.search(wt, l):
                            gender = self.genders[wt]
                            definition.setGender(gender)
                            break
                    inWord.setName(self.titleContent)
                    # Get rid of the word, we don't want it in the definition
                    l = re.sub(r"'''.*'''[ ]*(.*)", r"\1", l)
                    # Get rid of non wiki tags
                    l = re.sub(r'}}[^}]+{{', r'}} {{', l)
                    definition.addDescription("", 0, False)
                elif matching_word_nature:
                    if "flexion" not in l and matching_word_nature.group(1) in typesAllowed:
                        definition.setType(matching_word_nature.group(1).capitalize()) 
                        state=Wiktio.DEFINITION
                        toAdd = True
                elif matching_word_nature_bis:
                    if "flexion" not in l and matching_word_nature_bis.group(1) in typesAllowed:
                        definition.setType(matching_word_nature_bis.group(1).capitalize()) 
                        state=Wiktio.DEFINITION
                        toAdd = True
                elif matching_synonyme:
                    state=Wiktio.SYNONYME
                    synonyms = self.handleSynonyms(textSplitted)
                    definition.add(state, synonyms)
                    break
                #Pourquoi cette regexp ? Peutetre pour flexion (Regarder eclairci dans wiktionnaire)
                elif re.search(r"{{-.*-.*}}", l):
                    if not definition.rootDescription.isEmpty():
                        filterIndent = ""
                        definition = wiktio.Definition()
                        inWord.addDefinition(definition)
                    state = Wiktio.SKIP

                if state == Wiktio.SKIP:
                    continue

                if filterIndent != "":
                    # We are filtering, check this line is
                    # at a lower indentation level
                    result = re.search(r"^[ ]*[*#:;]+[ ]*", l)
                    if result:
                        if len(result.group(0).rstrip()) > len(filterIndent):
                            next = True
                        else:
                            filterIndent = ""
                    else:
                        filterIndent = ""


                if next:
                    continue

                # Categories
                if re.match(r"\[\[Catégorie:", l):
                    text = re.sub(r"\[\[Catégorie:([^|}\]]+).*", r"\1", l)
                    definition.add(Wiktio.CATEGORY, text)
                    continue

                if state == Wiktio.DEFINITION and startWithHash and not l.isspace():
                    [text, level, numbered] = self.wiki2xml(l, False, state)
                    definition.addDescription(text, level, numbered)
                elif state == Wiktio.SYNONYME:
                    [text, level, numbered] = self.wiki2xml(l, False, state)
                    definition.add(state, text)
                elif not startWithHash:
                    continue
                else:
                    if len(l) > 0:
                        definition.add(state, self.wiki2xml(l, True)[0], state)

        return inWord

# Set UTF-8 stdout in case of the user piping our output
importlib.reload(sys)
#sys.setdefaultencoding('utf-8')

usage = "usage: %prog [options] wiktionary_dump.xml word_list.txt"
parser = OptionParser(usage=usage)
parser.add_option("-o", "--output", dest="output",
              help="write result to file or directory")
(options, args) = parser.parse_args()

if len(sys.argv) < 4:
    parser.print_help()
    sys.exit()

wikiFile = sys.argv[1]
wordsFile = sys.argv[2]
output = sys.argv[3]

open(output, 'w').close()

# Import the list of words
f = open(wordsFile, "r")
words = []
wordslist = set([w.rstrip() for w in f.readlines()])


f.close()

_wiktio = wiktio.Wiktio()

outputSorted = output + "Sorted" 

try:
    parse(wikiFile, WikiHandler(wordslist, 'fr', _wiktio, output))
except Exception as e: print(e)

sortDicoFile(output, outputSorted)
os.rename(outputSorted, output)
splitDicoFile(output, 15000)
os.remove(output)
#with open(output, 'a+') as dictionnary:
#    dictionnary.write("</root>")

'''def sortchildrenby(parent, attr):
    parent[:] = sorted(parent, key=lambda child: child.get(attr))

parser = lxml.etree.XMLParser(strip_cdata=False)
tree = lxml.etree.parse(output, parser)
root = tree.getroot()

sortchildrenby(root, 'val')
for c in root:
    sortchildrenby(c, 'desc')
    #c[:] =  sorted(c, key=lambda child: (child.get('desc')))

outputSorted = output + "Sorted" 
open(outputSorted, 'w').close()

with open(outputSorted, 'a+', 0) as f:
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n")
    f.write (lxml.etree.tostring(root, encoding="utf-8", method="xml"))
    '''
