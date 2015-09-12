# pyatch - universal binary patch engine
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

import hashlib
import binascii

class Patcher:
    _version = 1.155#7273497909217
    
    def __init__(self, patchset=None):
        self.patchset = patchset
        self.patch = None
        self.filename = None
        self.filehash = None

    def use(self, fname):
        """set file name of patch target"""
        
        self.filename = fname

    def hash(self):
        """generate md5 hash of target file"""
        # source: http://stackoverflow.com/a/3431838

        if not self.filename:
            raise ValueError("no target file set. call use() first")
        
        h = hashlib.md5()
        with open(self.filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), ""):
                h.update(chunk)
        self.filehash = h.hexdigest()
        
        return self.filehash
    
    def getPatchForHash(self):
        """search in patchset for a patch with matching md5 hash"""
        
        if not self.filehash:
            raise ValueError("no hash set. call hash() first")

        # load patchset for file hash
        if self.filehash in self.patchset:
            self.patch = self.patchset[self.filehash]
        else:
            raise ValueError("no patch data found for this binary")

        # check if patchset contains a reference to another patchset which should be included
        if "apply_reference" in self.patch:
            ref = self.patch["apply_reference"]
            if ref in self.patchset:
                print "[+] adding %d referenced patches from %s" % (len(self.patchset[ref]), ref)

                # append version strings
                v = None
                if "version" in self.patchset[ref] and "version" in self.patch:
                    v = "%s+%s" % (self.patch["version"], self.patchset[ref]["version"])
                
                # add that patchset's data to our patchset
                self.patch.update(self.patchset[ref])

                # set version
                if v:
                    self.patch["version"] = v
            else:
                raise ValueError("referenced patchset %s not found" % ref)

    def applyFilePatch(self):
        """patch target file with chosen patch"""
        
        if not self.patch:
            raise ValueError("no patch set. call getPatchForHash() first")

        if "version" in self.patch:
            print "[+] patch version:", self.patch["version"]
        
        # open file and patch each given offset
        places = 0
        with open(self.filename, "r+b") as f:
            for p in self.patch:
                # ignore "version" key etc.
                if not isinstance(p, int):
                    continue
                    
                self.applyPatch(file=f, offset=p, data=self.patch[p])
                places += 1

        print "[+] patched %d places." % places

    def applyPatch(self, **kwargs):
        """patch a file object.
        mandatory keyword args:
        file: target file object
        offset: absolute offset in file
        data: list/tuple of bytes to replace the original bytes starting at offset"""
        
        f = kwargs["file"]
        o = kwargs["offset"]
        d = kwargs["data"]

        # offset must be numeric
        if not isinstance(o, int):
            raise ValueError("invalid offset %s" % o)

        # data should be a list/tuple
        if isinstance(d, tuple) or isinstance(d, list):
            pass
        elif isinstance(d, int): # single byte
            d = (d,)
        elif isinstance(d, str): # string of hex bytes
            try:
                d = map(ord, binascii.unhexlify(d))
            except TypeError as e:
                raise ValueError("invalid patch data %s -> %s" % (d, e))
        else:
            raise ValueError("invalid patch data %s" % d)

        print "[o] patching file offset 0x%08x with %d bytes" % (o, len(d))
        
        # go to offset
        f.seek(o)
        
        # write patch data
        for b in d:
            #print "[ ] writing 0x%x" % b
            f.write(chr(b))

    def patchOMatic(self, fname):
        """automatically search for patch in the patchset and apply it to the given target file"""

        print "[*] patcher version:", self._version
        
        self.use(fname)
        print "[*] using input file", self.filename
        
        # generate hash
        try:
            t = self.hash()
            print "[*] file hash:", t
        except IOError as e:
            print "!! IOError:", e
            return False

        # search patch set
        try:
            self.getPatchForHash()
        except ValueError as e:
            print "!! unknown file:", e
            return False

        # patch file
        try:
            self.applyFilePatch()
        except IOError as e:
            print "!! IOError:", e
            return False

        # generate new hash
        try:
            t = self.hash()
            print "[*] new file hash:", t
        except IOError as e:
            print "!! IOError:", e
            return False

        print "Success!"
        return True
