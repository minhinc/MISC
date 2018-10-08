for i in ${@:2}; do
python3 seed.py search $1 id $i > t.txt
python3 seed.py search $1 id $i > tt.txt
vi t.txt
ed -s t.txt << EOF
g/[ ]*$/s///
wq
EOF
diff t.txt tt.txt
echo "is it ok?"
read -n1 ans
if [ $ans == 'y' ]; then
python3 seed.py update $1 content "$(cat t.txt)" id $i
else
echo "bye $1"
exit
fi
done
