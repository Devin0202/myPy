# -*- coding: utf-8 -*-
"""
Language:   python3
Goal:       Convert UTF-8 to chinese string.
Reference:  https://docs.python.org/3/c-api/unicode.html
Brief:      PyObject* PyUnicode_AsRawUnicodeEscapeString(PyObject *unicode)
            Encode a Unicode object using Raw-Unicode-Escape and return the 
            result as a bytes object. Error handling is “strict”.
            Return NULL if an exception was raised by the codec.
Params:     "L\xE7\xBD\x97\xE9\xB8\xA3"
return:     L罗鸣
"""
import os
import sys
import time
print(sys.version)
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

### Defs region
def convert(utf8String):
    # theRaw = utf8String.encode("raw_unicode_escape")
    theRaw = bytes(utf8String, encoding = "raw_unicode_escape")
    return theRaw.decode("utf-8")

### Params region

ori = "L\xE7\xBD\x97\xE9\xB8\xA3"
print(type(ori))
print(ori)
print(convert(ori))

print(os.linesep)
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))