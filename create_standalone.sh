#!/bin/bash
# pyatch - create standalone patch script
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

set -e

if [ $# -ne 2 ]; then
    echo "Usage: $0 <patchset name> <target.py>"
    echo "Create standalone patch script"
    echo
    echo "patchset name: name of patchset in patchsets directory, e.g. 'example' for 'patchsets/example.py'"
    echo "target.py: name of generated standalone patch script"
    exit 1
fi

PATCHSET="$1"
PATCHSETFILE="patchsets/$1.py"
TARGET="$2"

PYATCHFILE="pyatch/__init__.py"

if [ -e "$TARGET" ]; then
    echo "$TARGET already exists."
    exit 2
fi

if [ ! -e "$PATCHSETFILE" ]; then
    echo "$PATCHSETFILE does not exist."
    exit 2
fi

if [ ! -e "$PYATCHFILE" ]; then
    echo "$PYATCHFILE does not exist."
    exit 2
fi

echo "Working ..."

# create target
cat autopatch.py > "$TARGET"

# replace patchset import
sed -i "/import patchsets/ {
    r $PATCHSETFILE
    d
}" "$TARGET"

sed -i 's/patchsets\.everything/patchset/g' "$TARGET"

# replace pyatch import
sed -i "/import pyatch/ {
    r $PYATCHFILE
    d
}" "$TARGET"

sed -i 's/pyatch\.//g' "$TARGET"

# remove #<csa_remove> ... #</csa_remove> blocks to remove e.g. test code from the resulting file
perl -pi -e 'BEGIN{undef $/;} s/#\s*<csa_remove>.*?#\s*<\/csa_remove>//sg' "$TARGET"

# remove # comments
sed -i 's/#.*$//g' "$TARGET"

# remove """ comments
perl -pi -e 'BEGIN{undef $/;} s/""".*?"""//sg' "$TARGET"

# remove empty/whitespace lines
sed -i '/^\s*$/d' "$TARGET"

# add shebang
sed -i '1s@^@#!/usr/bin/env python\n@' "$TARGET"

# add newline to end of file
sed -i '$a\' "$TARGET"

chmod 755 "$TARGET"
echo "$TARGET successfully created."
