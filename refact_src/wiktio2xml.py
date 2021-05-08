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

import importlib
import os
import re
import sys
from xml.sax import parse
from xml.sax.handler import ContentHandler

import wiktio
from sortFile import sortDicoFile
from splitFile import splitDicoFile
from wikimodele import *
from wikimodelearray import *
from wiktio import Wiktio

orthographic_constant = "Variante orthographique du mot "
pattern_to_split = "PATTERN_TO_SPLIT_BY"
def_end_str = "{{-EndOfDef-}}"

word_rank = 0
cpt = 0
debug = False


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
                if word.to_add is True:
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

    def get_synonyms(self, text):
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
        in_word = wiktio.Word()
        self.textContent = re.sub("(={2,} {)", pattern_to_split + r"\1", self.textContent)
        self.handle_by_sections(False, in_word, Wiktio.SKIP)
        return in_word

    def handle_by_sections(self, is_french_section, in_word, state):
        for text_split in re.split(r"%s" % pattern_to_split, self.textContent, flags=re.M | re.UNICODE):
            first_line = True

            # Append an end of text marker, it forces the end of the definition
            text_split += "\n" + def_end_str

            # Remove html comment (multiline)
            text_split = re.sub(r"<!--[^>]*-->", "", text_split, re.M)
            definition = wiktio.Definition()
            in_word.addDefinition(definition)
            concat = ""
            for line in text_split.splitlines():
                if not (is_french_section := self.check_french_section(line, is_french_section)):
                    break
                startWithHash = line.startswith("#")
                line = concat + line
                concat = ""

                if re.search(r"<[^>]+$", line):
                    # Wiki uses a trick to format text area by ending in incomplete
                    # html tags. In this case, we concat this line with the next one
                    # before processing it
                    concat = line
                    continue

                matching_synonym, matching_word_nature = self.init_regexp_syn_nature(line)

                if self.not_correct_first_line(first_line, matching_synonym, matching_word_nature):
                    break
                else:
                    first_line = False

                if matching_word_nature:
                    current_def = definition
                elif matching_synonym:
                    definition = current_def

                if self.handle_synonyms(definition, matching_synonym, text_split):
                    break

                self.handle_gender(definition, in_word, line, matching_word_nature)
                state = self.handle_type(definition, line, matching_word_nature, state, in_word)
                state = self.handle_last_line(line, state)

                if state == Wiktio.SKIP:
                    continue

                self.write_def_and_syn(definition, line, startWithHash, state)

    def init_regexp_syn_nature(self, line):
        # Retrieve nature of the word in line like === {{S|wordNature|fr(|.*optional)}} ===
        matching_word_nature = re.match(r"=== {{S\|([\w\W]*?)\|fr(\|.*)?}} ===", line, re.UNICODE)
        matching_synonym = re.match(r"==== {{S\|synonymes}} ====", line, re.UNICODE)
        return matching_synonym, matching_word_nature

    def write_def_and_syn(self, definition, line, startWithHash, state):
        if state == Wiktio.DEFINITION and startWithHash and not line.isspace():
            [text, level, numbered] = self.wiki2xml(line, False, state)
            definition.addDescription(text, level, numbered)
        elif state == Wiktio.SYNONYME:
            [text, level, numbered] = self.wiki2xml(line, False, state)
            definition.add(state, text)

    def handle_synonyms(self, definition, matching_synonym, text_split):
        if matching_synonym:
            state = Wiktio.SYNONYME
            synonyms = self.get_synonyms(text_split)
            definition.add(state, synonyms)
            return True
        return False

    def handle_last_line(self, line, state):
        if def_end_str in line:
            state = Wiktio.SKIP
        return state

    def handle_type(self, definition, line, matching_word_nature, state, in_word):
        if self.is_allowed_word(line, matching_word_nature):
            definition.setType(matching_word_nature.group(1).capitalize())
            state = Wiktio.DEFINITION
            in_word.set_to_add(True)
        return state

    def handle_gender(self, definition, inWord, line, matching_word_nature):
        if self.is_gender_line(self, line, matching_word_nature):
            self.define_gender(definition, line)
            inWord.setName(self.titleContent)

    #Return true if word's type belongs to typesAllowed
    @staticmethod
    def is_allowed_word(line, matching_word_nature):
        return matching_word_nature and "flexion" not in line and matching_word_nature.group(1) in typesAllowed

    #Return if the current line provides gender of the current word
    @staticmethod
    def is_gender_line(self, line, matching_word_nature):
        return re.match("'''" + self.titleContent + " ?'''", line)

    @staticmethod
    def not_correct_first_line(first_line, matching_synonym, matching_word_nature):
        return first_line and not matching_word_nature and not matching_synonym

    def define_gender(self, definition, line):
        for gender in list(self.genders.keys()):
            if re.search(gender, line):
                gender = self.genders[gender]
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
