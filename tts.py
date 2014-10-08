import os
import re

def generateScript(diPhone, reads, selects, count):
    if len(diPhone) == 1 and count == 0:
        reads += 'Read from file: "../sounds/-'+ diPhone  +'.wav" \n'
        reads += 'Rename: "difono'+ str(count) +'"\n'
        selects += 'select Sound difono'+ str(count) +'\n'
    elif len(diPhone) == 1 and count !=0:
        reads += 'Read from file: "../sounds/'+ diPhone +'-.wav"\n'
        reads += 'Rename: "difono'+ str(count) +'"\n'
        selects += 'plus Sound difono'+ str(count) +'\n'
    else:
        reads += 'Read from file: "../sounds/'+ diPhone +'.wav"\n'
        reads += 'Rename: "difono'+ str(count) +'"\n'
        selects += 'plus Sound difono'+ str(count) +'\n'
    return (reads, selects)
         
#string = "mamAsalAlapApa"
#string = "kAla"
string = 'papapApA'
sil = re.findall("([m|k|s|p|l][a|A]|\?)",string)
sil1 = re.findall("([a|A][m|k|s|p|l]|[m|k|s|p|l|a|A])",string)

for i,v in enumerate(sil):
    sil1.insert(2*i+1,v)

diPhones = sil1
reads = ''
selects = ''
count = 0

for diPhone in diPhones:
    (reads,selects) = generateScript(diPhone, reads, selects, count)
    count+=1

selects += 'Concatenate recoverably'
print reads
print selects

f = open('synthesis.praat', 'w')
f.write(reads)
f.write(selects)
f.close()


    

