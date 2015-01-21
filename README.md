# gfs-torrent
scripts for distributing GFS files trough bittorrent


## mktorrent-gfs-0.25.py

This script poll the FTPPRD server for new files, download them and make .torrent files

Usage : `./mktorrent-gfs-0.25.py {run}`

Example : `./mktorrent-gfs-0.25.py 2015011706` will create torrent files for the run 2015-01-16 06h.

Dependencies : `sudo apt-get install mktorrent`


## download-gfs-0.25.py

This script poll the torrent.openwindmap.org server for new torrent files, and download them.
Once the download is complete, a temp file named "grib_download_ok" is created. The script then continue seeding for 6 hours before exiting.

Usage : `./download-gfs-0.25.py {run} {max_hour}`

Example : `./download-gfs-0.25.py 2015011706 72` will download grib files 0 to 72.

Dependencies : `sudo apt-get install python-libtorrent`

Integration in a bash script :
```bash
#!/bin/bash

RUN=2015011706
LEN=72

# kill previous instance if still running
killall download-gfs-0.25.py  >& /dev/null

# remove state file
rm grib_download_ok >& /dev/null

# start downloading and seeding in a background process
./download-gfs-0.25.py $RUN $LEN &

# wait until the download is finished
while [ ! -e "grib_download_ok" ]; do
  sleep 1
done

# now run your stuf
# ungrib.exe / wrf …

```

