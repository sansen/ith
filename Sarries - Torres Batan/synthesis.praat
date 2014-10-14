Read from file: "sounds/-m.wav" 
Rename: "difono0"
Read from file: "sounds/ma.wav"
Rename: "difono1"
Read from file: "sounds/a-.wav"
Rename: "difono2"
select Sound difono0
plus Sound difono1
plus Sound difono2
Concatenate recoverably
select Sound chain
Save as WAV file... scripts/chain.wav
select TextGrid chain
Save as short text file... scripts/SegmentList.txt