#!usr/bin/sh
echo This script will download the latest LITE DB from ip2location.com
read login
read pass
read targetdir
wget "http://www.ip2location.com/download?productcode=DB11LITE&login=$login&password=$pass" --output-document=$targetdir
$targetdir/geoip.zip -package DB11LITE -login $login -password $pass && unzip $targetdir/geoip.zip
python preprocess.py $targetdir/IP2LOCATION-LITE-DB11.CSV | python reduce.py | perl generate_mmdb.pl neustar > $targetdir/geoip.mmdb
