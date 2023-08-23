#!/usr/bin/python

#
# @BEGIN LICENSE
#
# Psi4: an open-source quantum chemistry software package
#
# Copyright (c) 2007-2023 The Psi4 Developers.
#
# The copyrights for code used from other parties are included in
# the corresponding files.
#
# This file is part of Psi4.
#
# Psi4 is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, version 3.
#
# Psi4 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with Psi4; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# @END LICENSE
#

import glob
import os
import re
import sys

DriverPath = ''
InsertPath = '/../../../'
if (len(sys.argv) == 2):
    DriverPath = sys.argv[1] + '/'
    sys.path.insert(0, os.path.abspath(os.getcwd()))


def pts(category, pyfile):
    print('Auto-documenting %s file %s' % (category, pyfile))

# License file psi4/driver/source.template
fhead = open(DriverPath + '../../psi4/driver/source.template')
license = fhead.readlines()
fhead.close()

# Header file psi4/include/psi4/psifiles.h
pts('header', 'psifiles.h')

fhead = open(DriverPath + '../../psi4/include/psi4/psifiles.h')
contents = fhead.readlines()
fhead.close()

fpy = open(DriverPath + '../../psi4/driver/psifiles.py', 'w')
for line in license:
    fpy.write(line)
fpy.write('# Do not modify this file! It is auto-generated by the document_psifiles\n')
fpy.write('# script, from psi4topdir/psi4/include/psi4/psifiles.h\n')

psifDict = {}
goodfile = re.compile(r'^\s*#define\s+(\w+)\s+(\d+)\s+\/\*-\s+(.*)\s+-\*\/')

ii = 0
while (ii < len(contents)):
    line = contents[ii]

    if goodfile.match(line):
        psifLabel = goodfile.match(line).group(1)
        psifNumber = int(goodfile.match(line).group(2))
        psifComment = goodfile.match(line).group(3)

        fpy.write('%-27s = %4d  # %s\n' % (psifLabel, psifNumber, psifComment))

        psifDict[psifNumber] = {}
        psifDict[psifNumber]['label'] = psifLabel
        psifDict[psifNumber]['notes'] = psifComment

    ii += 1

fpy.write('\n')
fpy.close()


frst = open('source/autodoc_psifiles.rst', 'w')
frst.write('.. index:: psioh\n')
frst.write('.. _`apdx:psiFiles`:\n\n')
frst.write('PSIOH Intermediate Files\n')
frst.write('========================\n\n')
frst.write('.. table:: Auxiliary files in |PSIfour|\n\n')
frst.write('   +-%-4s-+-%-27s-+-%-120s-+\n' %
    (4 * '-', 27 * '-', 120 * '-'))
frst.write('   | %-4s | %-27s | %-120s |\n' %
    ('File', 'File Label', 'Contents'))
frst.write('   +=%4s=+=%27s=+=%120s=+\n' %
    (4 * '=', 27 * '=', 120 * '='))

for key in sorted(psifDict.keys()):
    frst.write('   | %4d | %-27s | %-120s |\n' %
        (key, psifDict[key]['label'], psifDict[key]['notes']))
    frst.write('   +-%-4s-+-%-27s-+-%-120s-+\n' %
        (4 * '-', 27 * '-', 120 * '-'))

frst.write('\n')
frst.close()
