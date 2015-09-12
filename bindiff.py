#!/usr/bin/env python
# pyatch - binary differ
# Copyright (C) 2015 szf <spezifisch@users.noreply.github.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
from math import log, ceil
import pyatch

def writeo(x):
    sys.stdout.write(x)

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    # source: http://stackoverflow.com/a/312464
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage:", sys.argv[0], "<reference file> <compared file>"
        sys.exit(1)

    fna = sys.argv[1]
    fnb = sys.argv[2]

    # get file sizes
    try:
        fnasize = os.stat(fna).st_size
        fnbsize = os.stat(fnb).st_size
    except OSError as e:
        print "!! OSError:", e
        sys.exit(1)

    comparesize = min(fnasize, fnbsize)
    if fnasize != fnbsize:
        print "!! file sizes differ. this is not fully supported. we only compare until the the end of the smaller file"

    # get hash of reference file
    p = pyatch.Patcher()
    p.use(fna)
    hasha = p.hash()

    # create patch
    patch = dict()
    try:
        with open(fna, "rb") as fa, open(fnb, "rb") as fb:
            file_curpos = 0 # file position
            patch_curoffset = -42
            patch_lastpos = -42

            print "processing ...",

            for file_curpos in range(comparesize):
                if file_curpos % 1024**2 == 0:
                    print ".",
                    sys.stdout.flush()

                if file_curpos != fa.tell() or file_curpos != fb.tell():
                    print "\nfile positions out of sync! curpos=%d fa=%d fb=%d" % \
                        (file_curpos, fa.tell(), fb.tell())

                # snail speed
                va = ord(fa.read(1))
                vb = ord(fb.read(1))

                # bytes differ
                if va != vb:
                    if patch_lastpos + 1 != file_curpos:
                        # start of data for a new offset
                        patch_curoffset = file_curpos
                        patch[patch_curoffset] = [vb,]
                    else:
                        # continuation of data for previous offset
                        patch[patch_curoffset].append(vb)

                    patch_lastpos = file_curpos
    except IOError as e:
        print "\n!! IOError:", e
        sys.exit(1)

    # expand offsets to .. places
    fs = max(fnasize, fnbsize)
    offset_places = int(ceil(log(fs)/log(16)))

    print "\ndone, here's your patch:"

    # show patch in our patchset format
    tw = 4 # tabwidth, beauty has its price
    print tw*" " + "# %s" % fna
    print tw*" " + "\"%s\": {" % hasha
    print 2*tw*" " + "\"version\": 1,"

    for offset in sorted(patch.keys()):
        # print offset with leading zeroes depending on file size
        fmt = "0x%%0%dx" % offset_places
        print 2*tw*" " + fmt % offset + ": ",

        # print data
        if len(patch[offset]) == 1:
            # single byte
            print "0x%02x," % patch[offset][0]
        else:
            # more bytes
            bytes_per_line = 13     # new line every ..th element
            line = 0
            
            writeo("(")
            for pchnk in chunks(patch[offset], bytes_per_line):
                # nice indentation: 2 tabs, "0x", offset, ": ("
                pre = ",\n" + (2*tw + 2 + offset_places + 3)*" "
                if line == 0:
                    pre = ""

                writeo(pre + ", ".join(["0x%02x" % b for b in pchnk]))

                line += 1
            writeo("),\n")

    print tw*" " + "},"
