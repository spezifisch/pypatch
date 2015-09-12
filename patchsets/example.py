# pyatch - example patchset
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

# a patchset consists of a dictionary whose keys are md5 hashs of the original binaries and the values
# are dictionaries with the patch information.
# the patch information contains a version number (just for display), the other keys are starting offsets
# in the original binary, their values are lists/tuples with the bytes that should replace the original data.

# in order to use the autopatcher you need to add this file to __init__.py

patchset = {
    # some binary
    "2eb1a3e346933962bdfbb7b118404b68": {
        "version": 5,               # just for info, optional
        0x2034: (0x12, 0x34, 0x56), # tuple of bytes
        0x0: (23, 42, 13, 5),       # decimal is possible, of course
        0x10dead: (0x90,),
        0x10deae: [0x90,],          # list of bytes
        0x10deaf: 0x90,             # one single byte
        0x10deac: "90",             # one byte as hex string
        0x10bef0: "2342beef",       # multiple bytes as hex string
    },
    # another binary
    "5788be1014ef2f7fbcfa95802afc9000": {
        0x10: (0x20, 0x30, 0x40),
    },
    # echo foobar > test
    "14758f1afd44c09b7992073ccf00b43d": {
        "version": 1,
        3: (0x41, 0x42, 0x43),
    },
    "d70fcb3e4852fd340348341af834f525": {
        "version": "yogurt",        # a string
                                    # include the patches from the specified hash,
                                    # no recursions, only one reference per patch
        "apply_reference": "14758f1afd44c09b7992073ccf00b43d",
        0x10: (0x41, 0x42, 0x43),   # you may still add additional patches
    },
}

# the following part is excluded when creating a standalone patcher with create_standalone.sh:
#<csa_remove>
foo = 42
#</csa_remove>
