#!/bin/bash
#args=("$@")
#$2 ${args[@]:3}
if [ $1 = "-f" ]; then
 shift 1
elif [[ $1 = "put" ]] && wget -q --method=HEAD http://www.minhinc.com/${2}/$(basename ${3}); then
 echo "File exists please use ftp.sh -f ..."
 read -p "Press (y/n) to override ... " yorno
 if [[ $yorno != "y" && $yorno != "Y" ]]; then
  exit -1
 fi
fi
HOST='minhinc.com'
USER='pravinkumarsinha'
PASSWD=`head -5 ~/passwd|tail -1`
ftp -inv $HOST << !
quote USER $USER
quote PASS $PASSWD
cd public_html/${2}
bin
$1 ${@:3}
quit
!
