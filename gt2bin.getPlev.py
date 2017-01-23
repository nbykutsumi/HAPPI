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
          #"ALL":[2006]
          "ALL":range(2007,2015+1)
         }

lvar   = ["u","v"]

nx, ny = 256, 128
lz     = [7]
#lz     = [3,7,10]

dplev  = {
 1:  1000.0
,2:  925.00
,3:  850.00
,4:  775.00
,5:  700.00
,6:  600.00
,7:  500.00
,8:  400.00
,9:  300.00
,10: 250.00
,11: 200.00
,12: 150.00
,13: 100.00
,14: 70.000
,15: 50.000
,16: 30.000
,17: 20.000
,18: 10.000
}

def ret_tstp(var):
    if var in ["T250","T500","T850","prcp","slp","u250","u850","v250","v850"]:
        return "6hr"
    elif var in ["q","u","v"]:
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
            for iz in lz:
                tstp = ret_tstp(var)
                ntime= ret_nz(tstp)
    
                if tstp == "mon":
                    srcDir = os.path.join(ibaseDir,runName,"y%04d"%Year)
                else:
                    srcDir = os.path.join(ibaseDir,runName,"y%04d"%Year,tstp)
           
                srcPath = os.path.join(srcDir,var)
    
                outDir  = os.path.join(obaseDir,runName,"y%04d"%Year,tstp)
                tmpPath = os.path.join(outDir, "%s%d.na.%dx%dx%d"%(var,int(dplev[iz]),ntime,ny,nx))
                outPath = os.path.join(outDir, "%s%d.sa.%dx%dx%d"%(var,int(dplev[iz]),ntime,ny,nx))
                util.mk_dir(outDir)
                print "Load"
                print srcPath
                print os.path.exists(srcPath) 
                cmd = "ngtconv -z %d -f raw_float_little %s %s"%(iz, srcPath, tmpPath)
                subprocess.call(cmd.split(" "))
    
                # Flip
                aIn = fromfile(tmpPath, float32).reshape(ntime,ny,nx)
                aIn[:,::-1,:].tofile(outPath)
                print "Write"
                os.remove(tmpPath)
                print "Write"
                print outPath
    
    
