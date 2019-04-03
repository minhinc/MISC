cdir=`pwd` 
if [ $# -eq 0 ]; then
cd ~
alpine -p ./pinerc.pmi
else
su - pravin -c "alpine -p ../pi/pinerc.pmi"
fi
cd $cdir
