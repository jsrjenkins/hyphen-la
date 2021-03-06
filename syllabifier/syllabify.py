#!/usr/bin/env python3

"""
    Syllabification script

    Copyright (C) 2016 Elie Roux

    Permission is hereby granted, free of charge, to any person obtaining a copy of
    this software and associated documentation files (the "Software"), to deal in
    the Software without restriction, including without limitation the rights to
    use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
    of the Software, and to permit persons to whom the Software is furnished to do
    so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

    Depends on pyphen: http://pyphen.org/
    You also need the hyph_la_liturgical.dic file. To get it, get the
      hyphen-la project on https://github.com/gregorio-project/hyphen-la
      and run "make" in the "patterns" directory.

"""

import pyphen
import argparse
import sys
import re

parser = argparse.ArgumentParser(
    				description='A script to "syllabify" (insert a character between all syllables) a file.',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-t', '--text-type',
                    help='text type (chant or prose)',
                    default='chant', dest='type')
parser.add_argument('-m', '--hyphen-mode',
                    help='Hyphenation mode (liturgical, phonetic or etymology)',
                    default='liturgical', dest='mode')
parser.add_argument('-i', '--input', nargs='?', type = argparse.FileType('r'),
					default=sys.stdin, dest='inputfile')
parser.add_argument('-o', '--output-file', nargs='?', type=argparse.FileType('w'),
                    default=sys.stdout, dest='outputfile')
parser.add_argument('-c', '--hyphen-char', nargs='?',
                    default='-', dest='hyphenchar')

args = parser.parse_args()

righthyphenmin = 2
lefthyphenmin = 2
cutvowels = False
if (args.type == 'chant'):
	righthyphenmin=1
	lefthyphenmin=1
	cutvowels = True

hyphenator = pyphen.Pyphen(filename='../patterns/hyph_la_'+args.mode+'.dic',left=lefthyphenmin,right=righthyphenmin)

def hyphenate_one_word(word):
	global hyphenator,args
	return hyphenator.inserted(word,args.hyphenchar)

wordregex = re.compile(r'\b[^\W\d_]+\b')

for line in args.inputfile:
	line = line.strip()
	hyphenline = wordregex.sub(lambda match: hyphenate_one_word(match.group(0)), line)
	args.outputfile.write(hyphenline+'\n')

args.inputfile.close()
args.outputfile.close()
