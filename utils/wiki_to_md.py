#!/usr/bin/env python3
# -*- coding: utf8 -*-

import os
import re

pre = re.compile(r'</?pre>',re.IGNORECASE)              # <pre>xxx</pre> -> ``` xxx ```
code = re.compile(r'</?code>',re.IGNORECASE)              # <code>xxx</code> -> ` xxx `
nowiki = re.compile(r'</?nowiki>',re.IGNORECASE)              # <nowiki>xxx</nowiki> -> xxx 
h4 = re.compile(r'^====')                               # ==== xxx ==== -> ### xxx
h3 = re.compile(r'^===')
h2 = re.compile(r'^==')
hd = re.compile(r'=+ *(?:$)')
ep = re.compile(r'\'\'\'')                              # '''xxx''' -> ***xxx***
ei = re.compile(r'\'\'')                                # ''xxx'' -> *xxx*
quot1 = re.compile(r'\[(https?)([^\] \t]+)\s+([^\]]+)\]',re.I)    # [http:xxx abc] -> [abc](http:xxx)
quot = re.compile(r'\[\[(?:[^\]]+\|)?([^\]]+)\]\]')                      # [[xxx|abc]] -> [abc]()
quotpre = re.compile(r'\[\[((?:(?:File:)|(?:Image:))(?:[^\]]+))\]\]',re.I)  # [[img]] -> ![img]()

with open(r'input.txt','r',encoding='utf8') as inputFile, open(r'output.txt','w',encoding='utf8',newline='\n') as outputFile:
    for indata in inputFile:
        if indata.startswith('{{'):
            continue
        indata = pre.sub(r'```',indata)
        indata = nowiki.sub(r'',indata)
        indata = code.sub(r'`',indata)
        indata = h4.sub(r'####',indata)
        indata = h3.sub(r'###',indata)
        indata = h2.sub(r'##',indata)
        indata = hd.sub(r'',indata)
        indata = ep.sub(r'**',indata)
        indata = ei.sub(r'*',indata)
        indata = quotpre.sub(r'![\1]()',indata)
        indata = quot1.sub(r'[\3](\1\2)',indata)
        indata = quot.sub(r'[\1]()',indata)
        outputFile.write(indata)
