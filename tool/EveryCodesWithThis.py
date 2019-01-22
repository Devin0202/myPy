# -*- coding: utf-8 -*-
"""
XXXXXXXXX
"""
import sys
import os
import time

### Definition region(Class, Functions, Constants)

if "__main__" == __name__:
    print(sys.version)
    timeStampFormat = "%Y-%m-%d %H:%M:%S"
    print(time.strftime(timeStampFormat, time.localtime()))
    ### Parameters region

    ### Job region
    print("Do something here~")
    pass

    print(os.linesep)
    print(time.strftime(timeStampFormat, time.localtime()))