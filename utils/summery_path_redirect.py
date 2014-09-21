#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os
import re

cd = re.compile(r'\]\([^/]+')   # dir/ -> ./
ext = re.compile(r'\.md')       # .md -> .html

with open(r'input.txt','r',encoding='utf8') as inputFile, open(r'output.txt','w',encoding='utf8',newline='\n') as outputFile:
    for indata in inputFile:
        indata = cd.sub(r'](.',indata.lstrip())
        indata = ext.sub(r'.html',indata.lstrip())

        outputFile.write(indata)
