#! /usr/bin/env python3
# -*- coding: utf8 -*-

import os
import sys
import os.path
import re

BASEPATH = r'.'

def rename(f):
    if not f.endswith('.md'):
        return
    ti = re.compile(r'^(##+)')
    data=''
    with open(f,'r', encoding='utf8', newline='\n') as inputFile:
        for line in inputFile:
            data += ti.sub(r'#\1',line)
    with open(f,'w', encoding='utf8', newline='\n') as outputFile:
        outputFile.write(data)

def walkp(dir, *,callback=print):
    for (path, dirs, files) in os.walk(dir):
        for f in files:
            callback(os.path.join(path,f))
        for d in dirs:
            walkp(d)

if __name__ == '__main__':
    if len(sys.argv) > 2:
        walkp(sys.argv[1], callback=rename)
    elif len(sys.argv) > 1:
        walkp(sys.argv[1])
    else:
        walkp(BASEPATH)

