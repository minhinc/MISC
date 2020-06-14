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
export SSHPASS=`head -5 ~/passwd|tail -1`
sshpass -e sftp -oBatchMode=no -b - pravinkumarsinha@minhinc.com << !
cd public_html/${2}
$1 ${@:3}
bye
!
