if [[ $# -eq 0 ]]; then
echo "--usage--"
echo "./arg.sh <[m|d]> <[agenda|php|pdf]> <[qt|c|cpp|gl|li|[Aa]ll>"
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
py=("1 2 3:L" "4 5 6:7 L" "8 9:L" "10 11:L" "12 13:L")
alltech[py]=py[@]
ldd=("1 2:L" "3 4:L" "5 6:L" "7 8:L" "9 10:L")
alltech[ldd]=ldd[@]

backend=''
under=''

if [ $1 == 'm' ]; then
 echo $'---- Mobile backend ----'
 backend='_m'
else
 echo $'---- Desktop backend ----'
fi

for i in "${!alltech[@]}"; do
 if [ $3 == ${i} ] || echo ${3}|egrep '^[Aa]ll'; then
  value=${alltech[$i]}
  python3 agenda.py $1 $2 $i "$under" "${!value}"
  if [ $2 == "php" ]; then
   ~/tmp/ftp.sh put training/${i} advance-${i}-slides${backend}.txt
  elif [ $2 == "pdf" ]; then
   ~/tmp/ftp.sh put training ${i}_pdf.html
  fi
 fi
done
