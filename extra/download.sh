#!/bin/bash
if [[ $# -lt 1 ]]; then
 echo -e "----usage---\ndownload.sh <url> <destinationdir>\ndownload.sh https://python-course.eu/machine_learning_data_visualization.php data/python-course"
else
 baseurl=`echo $1|sed 's/\(.*\/\).*/\1/'`
 file=`echo $1|sed 's/.*\/\(.*\)/\1/'`
 if [[ $# -lt 2 ]]; then
  dirname="./"
 else
  dirname="${2}/"
 fi
fi
if [ ! -e "$dirname" ]; then
 mkdir -p "$dirname"
 echo "created directory... ${dirname}"
fi
outputfile=`echo ${file} | awk -F '[.]\\\\w+$' '{print "'"$dirname"'" $1 ".txt"}'`
echo -e "baseurl -> ${baseurl}\nfile -> ${file}\ndirname -> ${dirname}\noutputfile -> ${outputfile}"
if echo ${baseurl}|grep 'doc.qt.io'; then
 if [ ! -e "$file" ]; then
  echo "fetching... ${baseurl}${file}"
  wget "${baseurl}${file}"
  ed -s "$file" <<< $'v/^<dd>/d\n,s/^[^"]*"\([^"]*\)".*/\\1/\nw'
 else
  echo "file available... ${file}"
 fi
 while read line; do
  outputfile=`echo ${line} | awk -F[.]html$ '{print "'"$dirname"'" $1 ".txt"}'`
  if [ -e "$outputfile" ] && [ -s "$outputfile" ]; then
   echo "file exists.. $outputfile"
  else
   pandoc "${baseurl}${line}" -f html -t plain -o "$outputfile" ; ed -s "$outputfile" <<< $'1,/QT DOCUMENTATION/d\n.,/^\s*$/d\n/The Qt Company Ltd. Documentation contributions included herein/,$d\n?\w*?+,$d\nw'
   echo "${baseurl}${line} >> $outputfile"
  fi
 done < "$file"
else
 if [ ! -e "$file" ]; then
  echo "fetching... ${baseurl}${file}"
  wget "${baseurl}${file}"
  pandoc "${baseurl}${file}" -f html -t plain -o "$outputfile"
 else
  echo "file available... ${file}"
 fi
fi
echo "over..."
