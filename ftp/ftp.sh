#!/bin/bash
#args=("$@")
#$2 ${args[@]:3}
if [ $1 = "-f" ]; then
 shift 1
elif [[ $1 = "put" ]] && wget -q --method=HEAD http://www.minhinc.000webhostapp.com/${2}/$(basename ${3}); then
 echo "File exists please use ftp.sh -f ..."
 read -p "Press (y/n) to override ... " yorno
 if [[ $yorno != "y" && $yorno != "Y" ]]; then
  exit -1
 fi
fi
HOST=`head -2 ~/passwd|tail -1|awk  -F"[ \t]" '{print $1}'`
echo "host $HOST"
USER=`head -2 ~/passwd|tail -1|awk  -F"[ \t]" '{print $2}'`
PASSWD=`head -2 ~/passwd|tail -1|awk  -F"[ \t]" '{print $3}'`
tnftp -inv $HOST << !
quote USER $USER
quote PASS $PASSWD
cd htdocs/${2}
bin
$1 ${@:3}
quit
!
