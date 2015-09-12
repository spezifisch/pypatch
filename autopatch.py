#!/usr/bin/env python
# pyatch - auto patcher
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

import pyatch
import patchsets

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print "Usage:", sys.argv[0], "<binary file to patch>"
        sys.exit(1)
        
    target = sys.argv[1]

    # create patcher instance with patchset containing everything in patchsets subdir
    p = pyatch.Patcher(patchsets.everything)

    # try to find correct patch and patch target file
    ok = p.patchOMatic(target)
    
    if not ok:
        print "Patch failed!"
        sys.exit(2)
