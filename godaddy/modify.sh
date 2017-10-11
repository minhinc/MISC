for i in `find . -name "*_.html"`; do
#echo $i
cp $i `echo $i|sed 's/\(.*\)_.html/\1.html/'`
f=`echo $i|sed 's/\(.*\)_.html/\1.html/'`
#echo $f
ed -s $f << EOF
/<body>/r !cat common
/<\/body>/-r !cat common_footer
wq
EOF
if [[ $f != "./home.html" ]] && [[ $f != "./about/home.html" ]] ; then
dirname=`echo $f|cut -d '/' -f2`
echo "dirname file" $dirname $f
if echo $f|egrep -q -i '(product|research|training|service|career|about)\/'; then
echo "processing "$f
ed -s $f << EOF
/color:#[0-9a-fA-F]*/s//color:X/
/li.*div.*div.*\/`echo $f|cut -d '/' -f2`\/home[.]htm.*color:X/s/X/#f38502
wq
EOF
fi
echo "..processing "$f
ed -s $f << EOF
g/=[ ]*"[.]\//s//="..\//g
wq
EOF
elif [[ $f == "./about/home.html" ]] ; then
ed -s $f << EOF
/color:#[0-9a-fA-F]*/s//color:X/
1
/li.*`echo $f|cut -d '/' -f2`\/home[.]htm.*color:X/s/X/#f38502
g/=[ ]*"[.]\//s//="..\//g
wq
EOF
fi
done

