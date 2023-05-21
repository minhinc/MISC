if [[ $# -eq 0 ]]; then
echo "--usage--"
echo "./arg.sh <[qt|c|cpp|gl|li|ldd|dp|[Aa]ll> <[companyname]> <[push]>"
exit
fi

declare -A alltech
qt=("1 2 3 4:L" "5 6 7 8:L" "9 10 11 12:L" "13 14 15 16: 17 L" "21 18 19: 20 L")
alltech[qt]=qt[@]
cpp=("1 2 3:4 L" "5 6:7 L" "8 9:10 L" "11 12:13 L" "14 15 16:17 18 L")
alltech[cpp]=cpp[@]
li=("1 2 3:L" "4 5:L" "6 7 8:L" "9 10 11:L" "12 13 14:L")
alltech[li]=li[@]
c=("1 2 3:L" "4 5 6:L" "7 8 9:L")
alltech[c]=c[@]
gl=("1 2 3 4:L" "5 6 7:8 9 L" "10:101 102 L")
alltech[gl]=gl[@]
qml=("1 2 3:4 L" "5 6 12:7 L" "8 9 10:11 13 L")
alltech[qml]=qml[@]
py=("1 2 3:L" "4 5 6:7 L" "8 9:10 L" "11 12 : L" "13 14:L")
alltech[py]=py[@]
ldd=("1 2:L" "3 4:L" "5 6:L" "7 8:L" "9 10:L")
alltech[ldd]=ldd[@]
dp=("1 2 3 4:L" "5:L" "6:L" "7:L")
alltech[dp]=dp[@]


for i in "${!alltech[@]}"; do
 if [ $1 == ${i} ] || echo ${1}|egrep '^[Aa]ll'; then
  value=${alltech[$i]}
  rm -rf logdir/advance-${i}-slides*.*
  if [[ ( ! -z "$2"  &&  "$2" != "push" ) ]]; then
   echo "---> python3 agenda.py --tech $1 --company $2 ${!value}"
   python3 agenda.py --tech $1 --company $2 "${!value}"
  else
   echo "---> python3 agenda.py --tech $1 ${!value}"
   python3 agenda.py --tech $1 "${!value}"
  fi
  count=0
  for ii in "${!value}"; do
   ii=`echo ${ii}|sed 's/:/ /g'`
   for j in $ii; do
    if [ "$j" -eq "$j" ] 2>/dev/null; then
     if [[ $count -eq 0 ]]; then
      argstr="${argstr} advance-${i}-slides.txt"
     else
      argstr="${argstr} advance-${i}-slides-chap${j}.txt"
     fi
    fi
    count=$((count+1))
   done
  done
  if [[ ( ! -z "$2"  &&  "$2" == "push" ) || ( ! -z "$3"  &&  "$3" == "push" ) ]]; then
  echo $argstr
  cd logdir
  ~/tmp/ftp.sh mput training/${i} $argstr `echo ${argstr}|sed 's/\(.txt\)/_m\1/g'` `echo ${argstr}|sed 's/\(.txt\)/_f\1/g'`
  ~/tmp/ftp.sh mput training advance-${i}-slides.pdf advance-${i}-slides_print.pdf
  fi
 fi
done
