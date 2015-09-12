# pyatch
Modular file patch engine in python.

Usage
-----

Let's create an example file.
```
% echo foobar > test
% md5sum test
14758f1afd44c09b7992073ccf00b43d  test
```

Add information how to patch it to `patchsets/example.py`:
```python
patchset = {
    # echo foobar > test
    "14758f1afd44c09b7992073ccf00b43d": {
        "version": 1,
        3: (0x41, 0x42, 0x43),
        },
}
```

When the patcher now sees a file with matching hash it replaces the bytes starting at offset 3 (bytes) with the bytes A, B, and C.

Let's try it:
```
% ./autopatch.py test
[*] using input file test
[*] file hash: 14758f1afd44c09b7992073ccf00b43d
[+] Using patch version: 1
[o] Patching file offset 0x00000003 with 3 bytes
[+] Patched 1 places.
[*] new file hash: da894c4ba8ff269b0cc33b23db6c5918
Success!

% cat test
fooABC
```

Standalone Patcher
------------------

You can also generate a standalone patcher. Though the generator script is not quite elegant.

```
% ./create_standalone.sh example tester.py
Working ...
tester.py successfully created.
```

You can now use the resulting script to patch the example file.
This results in the same output file as above as you can see from the MD5 hash.

```
% echo foobar > test
% ./tester.py test
[*] using input file test
[*] file hash: 14758f1afd44c09b7992073ccf00b43d
[+] Using patch version: 1
[o] Patching file offset 0x00000003 with 3 bytes
[+] Patched 1 places.
[*] new file hash: da894c4ba8ff269b0cc33b23db6c5918
Success!
```

Bindiff
-------

This tool compares two files of the same size and outputs a "patchset" compatible dictionary entry
which describes which offsets of the reference files have to be patched to obtain the target file.
You could insert the result into `patchsets/example.py` as is.

```
% cat test.before
foobar
% cat test.after
fooABC
% ./bindiff.py test.before test.after
processing ... . 
done, here's your patch:
        # test.before
        "14758f1afd44c09b7992073ccf00b43d": {
                "version": 1,
                0x3: (0x41, 0x42, 0x43),
        },
```
