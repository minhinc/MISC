if [ $# -lt 2 ]; then
 echo -e "usage:\ndifngit <minhinc.com dir> <file>\ndifngit misc abc.txt"
else
 cp "$2" "$2_orig"
 echo "######### fetching ${1}/${2} ###########"
 if ! ~/tmp/ftp.sh get $1 $2; then
 echo "$2 not at $1"
 rm "${2}_orig"
 exit -1
 fi
 diff "${2}_orig" "$2"
 if [ $? -ne 0 ]; then
  read -p "$2 <> push2git (y/n) ?" answer
  if [ $answer == 'y' ] || [ $answer == 'Y' ]; then
   git add $2
   echo "added ${2} to git, removing orig file"
  fi
 else
 echo "${2} no diff, removing dup"
 fi
 rm "${2}"
 mv "${2}_orig" $2
fi
