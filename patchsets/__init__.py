# pyatch - patchsets
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

# place all pyatch patchsets in this directory and add them here to use them with autopatcher

# dictionary containing all patchsets in this directory
everything = dict()

import example
everything.update(example.patchset)

#import something
#everything.update(something.patchset)

