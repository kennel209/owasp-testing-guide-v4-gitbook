#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os
import re
q = re.compile(r'\(([^\)]+)\)')     # ( ) -> %28 %29

with open(r'url.txt','r',encoding='utf8') as inputFile:
    outdata = ''
    for indata in inputFile:
        outdata+=q.sub(r'%28\1%29',indata)
        
with open(r'url.txt','w',encoding='utf8', newline='\n') as outputFile:        
    outputFile.write(outdata)
