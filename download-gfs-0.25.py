#!/usr/bin/python

import libtorrent as lt
import urllib2
import sys
import time

arg_run = str(sys.argv[1])
arg_len = int(sys.argv[2])
run_hour = arg_run[8:10]

files_wanted = []

if arg_len <= 240:
  for hour in range(0, arg_len+1, 3):
    filename = "gfs.t%sz.pgrb2.0p25.f%03d" % (run_hour, hour)
    files_wanted.append(filename)
else:
  for hour in range(0, 241, 3):
    filename = "gfs.t%sz.pgrb2.0p25.f%03d" % (run_hour, hour)
    files_wanted.append(filename)
  for hour in range(252, arg_len+1, 12):
    filename = "gfs.t%sz.pgrb2.0p25.f%03d" % (run_hour, hour)
    files_wanted.append(filename)


ses = lt.session()
ses.listen_on(6881, 6891)

torrents = []

last_url_check = 0

while 1:
  if int(time.time()) - last_url_check > 20:
    for f in files_wanted:
      url = "http://torrent.openwindmap.org/gfs-0.25/%s/%s.torrent" % (arg_run, f)
      print "test url", f
      try:
        torrent_file=urllib2.urlopen(url)
      except urllib2.HTTPError:
        continue
      
      print 'adding', f
      
      info = lt.torrent_info(lt.bdecode(torrent_file.read()))
      torrents.append(ses.add_torrent(info, "./"))
            
    for t in torrents:
      if t.name() in files_wanted:
        files_wanted.remove(t.name())
        
    last_url_check = int(time.time())
  
  remaining = 0
  for t in torrents:
    s = t.status()
    if t.is_seed():
      continue
    remaining += 1
    
    print t.name(), s.progress*100, s.download_rate/1000, s.upload_rate/1000, s.num_peers
  
  if (remaining == 0) and (len(files_wanted) == 0):
    print "download ok"
    open("grib_download_ok", 'w').close()
    break
  time.sleep(1)
  
print "now seeding"
time.sleep(60*60*6)

