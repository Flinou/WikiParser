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

import wiktio
from wiktio import Wiktio
from splitFile import splitDicoFile
from sortFile import sortDicoFile
import importlib

orthographic_constant = "Variante orthographique du mot "
pattern_to_split = "PATTERN_TO_SPLIT_BY"

word_rank = 0
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

    def __init__(self, search_words, locale, _wiktio, output_file):

        self.genders = {
            "{{m}}": "masculin",
            "{{f}}": "féminin",
            "{{mf}}": "masculin et féminin"
        }
        self.searchWords = search_words
        self.output = output_file
        self.origin = output_file
        self.locale = locale
        self.wiktio = _wiktio
        self.cpt = 0

        self.isPageElement = False

        self.isTitleElement = False
        self.titleContent = ""

        self.isTextElement = False
        self.textContent = ""
        self.previousLineExample = False

        self.little_level = 0
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

    def endElement(self, name):
        global word_rank
        global cpt
        word_rank = word_rank + 1
        if word_rank % 10000 == 0:
            print("Element " + str(word_rank) + " / 6600000")
        if name == 'page':
            self.isPageElement = False
            # Make self.titleContent a plain string for accent comparison (accented word not found in set if not used)
            self.titleContent = str(self.titleContent)
            if self.titleContent in self.searchWords:
                self.searchWords.remove(self.titleContent)
                word = self.parse_text()
                match_title_ctnt_space = "Notadded"
                match_title_ctnt_nmbr = "Notadded"
                if word and word.name:
                    # Remove words with space (expression for ex). Keep words with accent thanks to re.UNICODE trick
                    match_title_ctnt_space = re.match(".* .*", self.titleContent, re.UNICODE)
                if len(self.titleContent) > 1 and match_title_ctnt_space is None and toAdd == True:
                    self.wiktio.addWord(word)
                    self.wiktio.dump2html(self.output)
                    self.wiktio = wiktio.Wiktio()
                cpt = cpt + 1
                if cpt == 10000:
                    raise EndOfParsing
            self.titleContent = ""
            self.textContent = ""
        elif name == 'title':
            self.isTitleElement = False
        elif name == 'text':
            self.isTextElement = False

    def characters(self, ch):
        if self.isTitleElement:
            self.titleContent += ch
        elif self.isTextElement:
            self.textContent += ch

    # Returns a list [text, level, numbered]
    def indents2xml(self, text, as_text):
        numbered = False
        result = re.search(r"^[ ]*[*#:;]+[ ]*", text)
        if not result:
            self.little_level = 0
            return [text, self.little_level, numbered]

        indent = result.group(0).rstrip()
        self.little_level = len(indent)
        text = text[result.end():]

        if as_text:
            return [text, self.little_level, numbered]

        if indent[-1:] == "#":
            numbered = True

        return [text, self.little_level, numbered]

    # Replaces '''xx''' and ''xx'' from the given text
    # with openXml xx closeXml
    @staticmethod
    def quote2xml(quote, open_xml, close_xml, text):
        index = 0
        while index >= 0:
            index = text.find(quote)
            index2 = text.find(quote, index + len(quote))
            if index >= 0 and index2 >= 0:
                text = text.replace(quote, open_xml, 1)
                text = text.replace(quote, close_xml, 1)
            else:
                return text
        return text

    # Replace standard Wiki tags to XML
    # Returns a list [text, level, numbered]
    # numbered = True if this is a numbered list
    def wiki2xml(self, text, as_text, state):
        # Remove {{-}}, {{(}} and {{)}}
        text = re.sub(r"{{[-\)\(]}}", "", text)
        # Remove pattern like {{word:word}}
        text = re.sub(r"\[\[\w+:\w+\]\]", "", text)
        # Remove ref markup
        text = re.sub(r"<ref>[\w\W]*</ref>", "", text)
        if text == "":
            return self.indents2xml(text, as_text)

        [text, level, numbered] = self.indents2xml(text, as_text)
        text = re.sub(r"{{w\|([^}]+)}}", r"<i>\1</i>", text)

        isComment = re.match("^''[^']", text) or re.match("^'''''[^']", text) or re.match("^{{[\W\w]*}}''[^']", text)

        if text.startswith("{{"):
            # Find all patterns like : {{some text}} in line
            matchings = re.findall(r"{{[\w\W]+?}}", text)
            for match in matchings:
                # Check if pattern is like {{text| or {{text}} and if so save text (which is a precision for definition)
                precision = re.match("{{([\w\W]+?)(\||}})", match)
                if precision and precision.group(1):
                    precisionVal = precision.group(1)
                    # Check if the precision is worth adding in definition
                    if precisionVal in list(precisionsAllowed.keys()):
                        text = text.replace(match, precisionsAllowed[precisionVal])
                        # Remove all unrecognized wiki tags
        text = re.sub(r"{{[\w\W]*}}$", "", text)
        varianteOrtho = re.match(r"{{variante ortho de\|([\w\W]+?)}}", text)
        if varianteOrtho and varianteOrtho.group(1):
            text = orthographic_constant + varianteOrtho.group(1) + "."
        else:
            text = re.sub(r"{{[^}]+}}", "", text)

        text = self.make_text_italic_bold(text)
        # Get rid of Image
        lower_text = text.lower()
        if lower_text.startswith("[[image") or lower_text.startswith("[[fichier") or lower_text.startswith(
                "=") or lower_text.startswith("[[file"):
            text = ""
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
                text = text[:start] + text[pipe + 1:]
                text = text.replace("]]", "", 1)

        if state == Wiktio.SYNONYME:
            return [text, level, numbered]
        if isComment and self.previousLineExample:
            text = ""
            self.previousLineExample = True
        elif isComment and len(text) > 0:
            self.previousLineExample = True
        elif len(text) == 0 or str(text).isspace():
            self.previousLineExample = False
        else:
            text = text + "INS_NL_BEF"
            self.previousLineExample = False

        return [text, level, numbered]

    def make_text_italic_bold(self, text):
        text = self.quote2xml("'''", "<b>", "</b>", text)
        text = self.quote2xml("''", "<i>", "</i>", text)
        return text

    @staticmethod
    def check_french_section(line, is_french_section):
        matchingLangSection = re.match(r"==( ?){{langue\|(.*)}}( ?)==", line, re.UNICODE)
        if matchingLangSection:
            if matchingLangSection.group(2) == "fr":
                return True
            else:
                return False
        else:
            return is_french_section

    @staticmethod
    def synonym_string_creation(synonym, title, firstTitle):
        if firstTitle:
            synonym += title + " "
        else:
            synonym = re.sub(r', $', '', synonym)
            synonym += "<br>" + title + " "
        return synonym

    def handle_synonyms(self, text):
        synonym = ""
        firstTitle = True
        for line in text.splitlines():
            # Title are information about register for use of synonyms
            # Titles in synonyms section can be like '''Militaire''' or ; '''Militaire :'''
            matchingTitle = re.match(r";? *'{2,3}(.*?)\W?\:?'{2,3}", line, re.UNICODE)
            # Other title in synonym are like {{|Appareil portatif}}
            matchingOtherTitle = re.match(r"{{\|(.*)}}", line, re.UNICODE)
            if matchingTitle and not line.startswith("*"):
                title = "(" + matchingTitle.group(1) + ")"
                synonym = self.synonym_string_creation(synonym, title, firstTitle)
                firstTitle = False
            elif matchingOtherTitle and not line.startswith("*"):
                title = "(" + matchingOtherTitle.group(1) + ")"
                synonym = self.synonym_string_creation(synonym, title, firstTitle)
                firstTitle = False

            if line.startswith("*"):
                currentSyn = re.match(r".* \[\[(.*)\]\]", line, re.UNICODE)
                if currentSyn:
                    synonym += currentSyn.group(1) + ", "

        synonym = re.sub(r', $', '', synonym)
        return synonym

    # Wikipedia text content is interpreted and transformed in XML
    def parse_text(self):
        value = 0
        # print "Processing " + self.titleContent
        inWord = wiktio.Word()
        frenchSection = False
        global toAdd
        toAdd = False
        state = Wiktio.SKIP
        filterIndent = ""
        self.textContent = re.sub("(={2,} {)", pattern_to_split + r"\1", self.textContent)
        global current_def
        for text_split in re.split(r"%s" % pattern_to_split, self.textContent, flags=re.M | re.UNICODE):
            firstLine = True

            # Append an end of text marker, it forces the end of the definition
            text_split += "\n{{-EndOfTest-}}"

            # Remove html comment (multiline)
            text_split = re.sub(r"<!--[^>]*-->", "", text_split, re.M)
            definition = wiktio.Definition()
            inWord.addDefinition(definition)
            concat = ""
            for line in text_split.splitlines():
                # Check if in French part of definition, if not break
                frenchSection = self.check_french_section(line, frenchSection)
                if not frenchSection:
                    break
                startWithHash = False
                if line.startswith("#"):
                    startWithHash = True
                line = concat + line
                concat = ""
                next = False

                # Regarder le mot taf dans le wiktionnaire pour comprendre
                if re.search(r"<[^>]+$", line):
                    # Wiki uses a trick to format text area by ending in incomplete
                    # html tags. In this case, we concat this line with the next one
                    # before processing it
                    concat = line
                    continue
                # Retrieve nature of the word in line like === {{S|wordNature|fr(|.*optional)}} ===
                matching_word_nature = re.match(r"=== {{S\|([\w\W]*?)\|fr(\|.*)?}} ===", line, re.UNICODE)
                matching_synonym = re.match(r"==== {{S\|synonymes}} ====", line, re.UNICODE)

                if firstLine and not matching_word_nature and not matching_synonym:
                    break

                if matching_word_nature:
                    current_def = definition
                elif matching_synonym:
                    definition = current_def
                firstLine = False

                if line.startswith("'''" + self.titleContent + "'''") or line.startswith("'''" + self.titleContent + " '''"):
                    self.define_gender(definition, line)
                    inWord.setName(self.titleContent)
                    # Get rid of the word, we don't want it in the definition
                    line = re.sub(r"'''.*'''[ ]*(.*)", r"\1", line)
                    # Get rid of non wiki tags
                    line = re.sub(r'}}[^}]+{{', r'}} {{', line)
                    definition.addDescription("", 0, False)
                elif matching_word_nature:
                    if "flexion" not in line and matching_word_nature.group(1) in typesAllowed:
                        definition.setType(matching_word_nature.group(1).capitalize())
                        state = Wiktio.DEFINITION
                        toAdd = True
                elif matching_synonym:
                    state = Wiktio.SYNONYME
                    synonyms = self.handle_synonyms(text_split)
                    definition.add(state, synonyms)
                    break
                # Why that ? Maybe for flexion (Watch eclairci in wiktionary)
                elif re.search(r"{{-.*-.*}}", line):
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
                    result = re.search(r"^[ ]*[*#:;]+[ ]*", line)
                    if result:
                        if len(result.group(0).rstrip()) > len(filterIndent):
                            next = True
                        else:
                            filterIndent = ""
                    else:
                        filterIndent = ""

                if next:
                    continue

                if state == Wiktio.DEFINITION and startWithHash and not line.isspace():
                    [text, level, numbered] = self.wiki2xml(line, False, state)
                    definition.addDescription(text, level, numbered)
                elif state == Wiktio.SYNONYME:
                    [text, level, numbered] = self.wiki2xml(line, False, state)
                    definition.add(state, text)
                elif not startWithHash:
                    continue
                else:
                    if len(line) > 0:
                        definition.add(state, self.wiki2xml(line, True)[0], state)

        return inWord

    def define_gender(self, definition, line):
        for wt in list(self.genders.keys()):
            if re.search(wt, line):
                gender = self.genders[wt]
                definition.setGender(gender)
                break


importlib.reload(sys)
wikiFile = sys.argv[1]
wordsFile = sys.argv[2]
output = sys.argv[3]

open(output, 'w').close()

# Import the list of words
f = open(wordsFile, "r")
words = []
words_list = set([w.rstrip() for w in f.readlines()])

f.close()
_wiktio = wiktio.Wiktio()
outputSorted = output + "Sorted"

try:
    parse(wikiFile, WikiHandler(words_list, 'fr', _wiktio, output))
except Exception as e:
    print(e)

sortDicoFile(output, outputSorted)
os.rename(outputSorted, output)
splitDicoFile(output, 150000)
os.remove(output)
# with open(output, 'a+') as dictionnary:
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
