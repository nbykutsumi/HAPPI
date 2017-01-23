from numpy import *
import subprocess
import os,sys

model    = "MIROC5"
#ibaseDir = "/data2/hjkim/HAPPI"
#runName  = "%s-%s-%03d"%(prj,expr,ens)
#srcDir   = os.path.join(ibaseDir,runName,"y%04d"%Year)

srcDir   = "/home/utsumi/mnt/well.share/HAPPI/data/%s"%(model)
srcPath  = os.path.join(srcDir,"GTAXLOC.STDPL18")

Var      = "plev"

print srcPath
print os.path.exists(srcPath)
obaseDir = srcDir
tmpPath  = os.path.join(obaseDir, "temp.txt")

# Write to temp file
cmd  = "gtaxis %s -x -plain -text ncol=1 >%s"%(srcPath, tmpPath)
#cmd  = "gtaxis /home/utsumi/mnt/well.share/HAPPI/data/GTAXLOC.STDPL18 -x -plain -text ncol=1"
print cmd

os.chdir(obaseDir)
subprocess.call(cmd, shell=True)

# Load temp file and formatting
f=open(tmpPath,"r"); lines=f.readlines()[1:]; f.close()
lines = [s.strip() for s in lines]

# Flip (for lat)
if Var =="lat": lines = lines[::-1]

# Write
outPath  = os.path.join(obaseDir, "%s.txt"%(Var))
sout     = "\n".join(lines).strip()
f=open(outPath, "w"); f.write(sout); f.close()
print outPath

# Delete temp file
os.remove(tmpPath)
