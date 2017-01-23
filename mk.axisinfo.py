from numpy import *
import subprocess
import os,sys

model = "MIROC5"
prj   = "C20"
expr  = "ALL"
ens   = 1
Year  = 2006
var   = "Ts"

ibaseDir = "/data2/hjkim/HAPPI"
runName  = "%s-%s-%03d"%(prj,expr,ens)
srcDir   = os.path.join(ibaseDir,runName,"y%04d"%Year)
srcPath  = os.path.join(srcDir,var)


print srcPath
print os.path.exists(srcPath)
obaseDir = "/home/utsumi/mnt/well.share/HAPPI/data/%s"%(model)
tmpPath  = os.path.join(obaseDir, "temp.dat")
#for Var in ["lat","lon"]:
for Var in ["lat","lon"]:
    if   Var == "lat": sopt = "y"
    elif Var == "lon": sopt = "x"
    else: print "check Var", sys.exit()

    # Write to temp file
    cmd  = "gtaxis %s -%s -plain -text ncol=1 >%s"%(srcPath, sopt, tmpPath)
    print cmd
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
