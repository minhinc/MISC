tnftp -inv "ftpupload.net" << !
quote USER "epiz_30083730"
quote PASS "9kF49KhXHtP8q"
cd htdocs/${2}
bin
for i in tex.py; do
$1 ${i}
done
quit
!
{
 echo "epiz_30083730" "9kF49KhXHtP8q"
 echo bin
 echo prompt
 for i in ${@:3}; do
  echo cd htdocs
