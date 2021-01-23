import os
from utils.runscanDir import Recursion
def findFile(directory,indexFile):
        #print(directory,indexFile)
        targetIndex=Recursion(directory,indexFile)
        print(targetIndex)
        if targetIndex:
            return targetIndex
        else:
            return

