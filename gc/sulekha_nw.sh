searchline=""
rm test*.txt
if [[ $# -eq 0 ]]; then
echo "usage: ./sulekha.com  \"Embedded QT Training, Computer networking training\" "
exit -1
else
searchline=$1
fi
while read -r line; do
if echo $line|grep -i -q "$searchline"; then
echo $previousline | tee -a test.txt
elif echo $line|egrep -i -v -q '(^\s*$)|(^\s*[+]91)|(Review)|(Sulekha\s*Score)'; then
previousline=$line
fi
done < tmp.txt
cat test.txt|sort|uniq>test1.txt
mv test1.txt test.txt
