rm test*.txt
companyname="false"
list=""
while read -r line; do
if [ "$companyname" == "true" ] && echo $line|egrep -q -v '^\s*$'; then
companyname="false"
joblocation="true"
list="${list}$line"
fi
if [ "$joblocation" == "true" ] && echo $line|egrep -q -i 'Job\s*Location'; then
placename=`echo ${line}|awk -F Location '{print $2}'`
list="$list $placename"
echo $list | tee -a test.txt
list=""
fi
if echo $line|egrep -q '^\s*Company[ ]*Name\s*$'; then
companyname="true"
joblocation="false"
fi
done < tmp.txt
cat test.txt|sort|uniq>test1.txt
mv test1.txt test.txt
#echo -e $list >> test.txt
