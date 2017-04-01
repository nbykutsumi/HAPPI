from numpy import *
import myfunc.util as util
import subprocess
import calendar
import os,sys

model  = "MIROC5"
prj    = "C20"
#lexpr  = ["ALL","P15","P20"]
#lexpr  = ["P15","P20"]
lexpr  = ["P20"]

lens   = [11,21,31,41]

dlYear = {
           "ALL":range(2006,2015+1)
          ,"P15":range(2106,2115+1)
          ,"P20":range(2106,2115+1)
         }

ldat = []
#ldat.append([topo","sfc","const"])  # Reads CMIP5 now
ldat.append(["slp","6hr"])  # c.findcyclone
ldat.append(["u850","6hr"])  # c.findcyclone
ldat.append(["v850","6hr"])  # c.findcyclone
ldat.append(["Ts","mon"])  # tc.mk.tclist
ldat.append(["T850","6hr"])  # tc.mk.tclist, f.mk.potloc
ldat.append(["T500","6hr"])  # tc.mk.tclist
ldat.append(["T250","6hr"])  # tc.mk.tclist
ldat.append(["u850","6hr"])  # tc.mk.tclist
ldat.append(["u250","6hr"])  # tc.mk.tclist
ldat.append(["v850","6hr"])  # tc.mk.tclist
ldat.append(["v250","6hr"])  # tc.mk.tclist
ldat.append(["prcp","mon"])  # ms.mkRegion
ldat.append(["prcp","6hr"])  # ms.mkRegion

nx,ny  = 256, 128

def ret_nz(tstp):
    if   tstp == "6hr":return 1460
    elif tstp == "1dy":return 365
    elif tstp == "mon":return 12
    else:
        print "check tstp",tstp
        sys.exit()

#ibaseDir = "/data2/hjkim/HAPPI"
ibaseDir = "/data4/common/HAPPI"
obaseDir = "/home/utsumi/mnt/wellshare/HAPPI/data/%s"%(model)

lkeys = [[expr,ens] for expr in lexpr for ens in lens]
for expr, ens in lkeys:
    runName = "%s-%s-%03d"%(prj,expr,ens)
    for Year in dlYear[expr]:
        for [var,tstp] in ldat:
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


