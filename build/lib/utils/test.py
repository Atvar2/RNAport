from runscanDir  import Recursion
import sys,os

dir='/hwfswh2/BC_COM_P5/F19FTSCCWLJ2258/HICygxD/F20FTSCCKF1773_NICzjkE/00.ref/01.index'
file='refMrna.fa'
#file='refMrna.fa'
#dir='/hwfswh2/BC_COM_P5/F19FTSCCWLJ2258/HICygxD/F20FTSCCKF1773_NICzjkE/00.ref/01.index'
#t=Recursion(directory,indexFile)
targetIndex=Recursion(dir)

t=Recursion(dir)
print(t,'$$$$$$$$$$$$',targetIndex)
