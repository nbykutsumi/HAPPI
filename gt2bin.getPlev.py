from numpy import *
import myfunc.util as util
import subprocess
import calendar
import os,sys

model  = "MIROC5"
prj    = "C20"
#lexpr  = ["ALL","P15","P20"]
lexpr  = ["P20"]
lens   = [11,21,31,41]

dlYear = {
           "ALL":range(2006,2015+1)
          ,"P15":range(2106,2115+1)
          ,"P20":range(2106,2115+1)
         }

ldat  = []
ldat.append(["u",500,"1dy"])  # c.runmean
ldat.append(["v",500,"1dy"])  # c.runmean
ldat.append(["q",850,"1dy"])  # ms.FindMinMax
ldat.append(["q",500,"1dy"])  # ms.FindMinMax
ldat.append(["q",250,"1dy"])  # ms.FindMinMax


nx, ny = 256, 128
lz     = [7]
#lz     = [3,7,10]

#ibaseDir = "/data2/hjkim/HAPPI"
ibaseDir = "/data4/common/HAPPI"
obaseDir = "/home/utsumi/mnt/wellshare/HAPPI/data/%s"%(model)

diz  = {
  1000:1 
, 925 :2 
, 850 :3 
, 775 :4 
, 700 :5 
, 600 :6 
, 500 :7 
, 400 :8 
, 300 :9 
, 250 :10
, 200 :11
, 150 :12
, 100 :13
, 70  :14
, 50  :15
, 30  :16
, 20  :17
, 10  :18
}


def ret_nz(tstp):
    if   tstp == "6hr":return 1460
    elif tstp == "1dy":return 365
    elif tstp == "mon":return 12
    else:
        print "check tstp",tstp
        sys.exit()

lkeys = [[expr,ens] for expr in lexpr for ens in lens]
for expr, ens in lkeys:
    runName = "%s-%s-%03d"%(prj,expr,ens)
    for Year in dlYear[expr]:
        for [var,plev,tstp] in ldat:
            iz   = diz[plev]
            ntime= ret_nz(tstp)
    
            if tstp == "mon":
                srcDir = os.path.join(ibaseDir,runName,"y%04d"%Year)
            else:
                srcDir = os.path.join(ibaseDir,runName,"y%04d"%Year,tstp)
           
            srcPath = os.path.join(srcDir,var)
    
            outDir  = os.path.join(obaseDir,runName,"y%04d"%Year,tstp)
            tmpPath = os.path.join(outDir, "%s%d.na.%dx%dx%d"%(var,plev,ntime,ny,nx))
            outPath = os.path.join(outDir, "%s%d.sa.%dx%dx%d"%(var,plev,ntime,ny,nx))
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
    
    
