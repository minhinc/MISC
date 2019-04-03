cdir=`pwd`
if [ $# -eq 0 ]; then
cd ~
alpine -p ./pinerc.mi
else
su - sales -c "alpine -p ../pi/pinerc.mi"
fi
cd $cdir
