from numpy import *
import myfunc.util as util
import subprocess
import calendar
import os,sys

model  = "MIROC5"
prj    = "C20"
lexpr  = ["ALL"]
lens   = [1]

dlYear = {
          "ALL":range(2015,2016+1)
          #"ALL":range(2008,2016+1)
         }

lvar   = ["Ts"]
#lvar = ["T250","T500","T850","prcp","slp","u250","u850","v250","v850","Ts"]
#lvar   = ["slp"]

nx,ny  = 256, 128

def ret_tstp(var):
    if var in ["T250","T500","T850","prcp","slp","u250","u850","v250","v850"]:
        return "6hr"
    elif var in ["q"]:
        return "1dy"
    elif var in ["Ts"]:
        return "mon"

def ret_nz(tstp):
    if   tstp == "6hr":return 1460
    elif tstp == "1dy":return 365
    elif tstp == "mon":return 12
    else:
        print "check tstp",tstp
        sys.exit()

ibaseDir = "/data2/hjkim/HAPPI"
obaseDir = "/home/utsumi/mnt/wellshare/HAPPI/data/%s"%(model)

lkeys = [[expr,ens] for expr in lexpr for ens in lens]
for expr, ens in lkeys:
    runName = "%s-%s-%03d"%(prj,expr,ens)
    for Year in dlYear[expr]:
        for var in lvar:
            tstp = ret_tstp(var)
            nz   = ret_nz(tstp)

            if tstp == "mon":
                srcDir = os.path.join(ibaseDir,runName,"y%04d"%Year)
            else:
                srcDir = os.path.join(ibaseDir,runName,"y%04d"%Year,tstp)
       
            srcPath = os.path.join(srcDir,var)

            outDir  = os.path.join(obaseDir,runName,"y%04d"%Year,tstp)
            tmpPath = os.path.join(outDir, "%s.na.%dx%dx%d"%(var,nz,ny,nx))
            outPath = os.path.join(outDir, "%s.sa.%dx%dx%d"%(var,nz,ny,nx))
            util.mk_dir(outDir)
            print "Load"
            print srcPath
            print os.path.exists(srcPath) 
            cmd = "ngtconv -f raw_float_little %s %s"%(srcPath, tmpPath)
            subprocess.call(cmd.split(" "))

            # Flip and Unit
            aIn = fromfile(tmpPath, float32).reshape(nz,ny,nx)

            if var=="slp":
                aIn = aIn*1000.   # hPa --> Pa

            aIn[:,::-1,:].tofile(outPath)
            print "Write"
            os.remove(tmpPath)
            print "Write"
            print outPath


