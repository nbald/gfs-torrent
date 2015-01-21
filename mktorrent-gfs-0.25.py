#!/usr/bin/python

import ftplib
import sys
from subprocess import call
import time

def getftplist( run ):
  ftp = ftplib.FTP("ftpprd.ncep.noaa.gov")
  ftp.login("anonymous", "openwindmap.org")
  ftp.cwd("/pub/data/nccf/com/gfs/prod/gfs.%s" % run)

  files = []

  try:
      files = ftp.nlst()
  except ftplib.error_perm, resp:
      if str(resp) == "550 No files found":
          print "No files in this directory"
      else:
          raise
        
  ftp.quit();

  return files;



arg_run = str(sys.argv[1])
print "start", arg_run

run_hour = arg_run[8:10]

files_wanted = []

for hour in range(0, 241, 3):
  filename = "gfs.t%sz.pgrb2.0p25.f%03d" % (run_hour, hour)
  files_wanted.append(filename)

for hour in range(252, 385, 12):
  filename = "gfs.t%sz.pgrb2.0p25.f%03d" % (run_hour, hour)
  files_wanted.append(filename)


while len(files_wanted) > 0:
  start_time = int(time.time())
  
  files_available = getftplist(arg_run)
  files_downloaded = []

  for f in files_wanted:
    if f in files_available :
      print "file", f   
      url = "ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.%s/%s" % (arg_run, f)
      returncode = call(["aria2c", "-x 4", "--allow-overwrite=true", url])
      if returncode == 0:
        files_downloaded.append(f)
        call(["mktorrent",
              f,
              "-a http://torrent.openwindmap.org:6969/announce",
              "-w http://ftpprd.ncep.noaa.gov/data/nccf/com/gfs/prod/gfs.%s/%s" % (arg_run, f)
              ])
        call(["rm", f])
        call(["mv", "%s.torrent" % f, "/opt/torrent/pub/gfs-0.25/%s/" % arg_run])
      
  for f in files_downloaded:
    files_wanted.remove(f)

  loop_time = int(time.time()) - start_time
  if loop_time < 20:
    wait_time = 20 - loop_time 
    print "wait", wait_time
    time.sleep(wait_time)
  print "loop"
