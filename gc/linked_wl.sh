rm test*.txt
companyname="false"
list=""
while read -r line; do
if [ "$companyname" == "true" ] && echo $line|egrep -q -v '^\s*$'; then
companyname="false"
joblocation="true"
list="${list}$line"
elif [ "$joblocation" == "true" ]; then
if echo $line|egrep -q -i ',.*More'; then
placename=`echo ${line}|awk -F More '{print $1}'`
else
placename=$line
fi
list="$list $placename"
echo $list | tee -a test.txt
list=""
companyname="false"
joblocation="false"
elif echo $line|egrep -q '^\s*[0-9][0-9]*d\s*$'; then
companyname="true"
joblocation="false"
fi
done < tmp.txt
cat test.txt|sort|uniq>test1.txt
mv test1.txt test.txt
ed -s test.txt <<< $'g/ä/s//a/g\nwq'
ed -s test.txt <<< $'g/â/s//a/g\nwq'
ed -s test.txt <<< $'g/ā/s//a/g\nwq'
ed -s test.txt <<< $'g/á/s//a/g\nwq'
ed -s test.txt <<< $'g/ą/s//a/g\nwq'
ed -s test.txt <<< $'g/Ā/s//A/g\nwq'
ed -s test.txt <<< $'g/é/s//e/g\nwq'
ed -s test.txt <<< $'g/è/s//e/g\nwq'
ed -s test.txt <<< $'g/í/s//i/g\nwq'
ed -s test.txt <<< $'g/ī/s//i/g\nwq'
ed -s test.txt <<< $'g/İ/s//I/g\nwq'
ed -s test.txt <<< $'g/ł/s//l/g\nwq'
ed -s test.txt <<< $'g/ñ/s//n/g\nwq'
ed -s test.txt <<< $'g/ö/s//o/g\nwq'
ed -s test.txt <<< $'g/ó/s//o/g\nwq'
ed -s test.txt <<< $'g/ô/s//o/g\nwq'
ed -s test.txt <<< $'g/ü/s//u/g\nwq'
ed -s test.txt <<< $'g/ú/s//u/g\nwq'
ed -s test.txt <<< $'g/ş/s//s/g\nwq'
ed -s test.txt <<< $'g/jobs[ ]*>$/s///\nwq'
#echo -e $list >> test.txt
