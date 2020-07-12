#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import unittest

class TestStringMethods(unittest.TestCase):
    def test_regression_xml(self):
        self.assertTrue(isDifferent.isspace())

os.system("../src/wiktio2xml.py  ../wiktionnaryDump/frwiktionary-20200501-pages-articles.xml ../wordsList/lightwords ../dictionnaryOutput/dictionnaire")
isDifferent = subprocess.check_output("xmldiff ../dictionnaryOutput/dictionnaire ../dictionnaryOutput/dictionnaire_1307_0049", shell=True)
unittest.main()
