#args=("$@")
#$2 ${args[@]:3}
export SSHPASS=`head -5 ~/passwd|tail -1`
sshpass -e sftp -oBatchMode=no -b - pravinkumarsinha@minhinc.com << !
cd public_html/${2}
$1 ${@:3}
bye
!
