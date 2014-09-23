#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os
import re

cd = re.compile(r'\[([^\(\[]+)\s*(?:\(([^\(]+)\))?\]')   # [xxx(yyy)]/ -> yyy xxx

with open(r'input.txt','r',encoding='utf8') as inputFile, open(r'output.txt','w',encoding='utf8',newline='\n') as outputFile:
    for indata in inputFile:
        result = cd.search(indata.lstrip())
        if result:
            if result.group(2):
                outputFile.write(result.group(2)+'\t'+result.group(1)+'\n')
            else:
                outputFile.write('\t\t'+result.group(1)+'\n')