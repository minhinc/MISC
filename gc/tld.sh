#Afghanistan	.af
#Aland Islands	.ax
#Albania	.al
#Algeria	.dz
#American Samoa	.as
#Andorra	.ad
#Angola	.ao
#Anguilla	.ai
#Antarctica	.aq
#Antigua and Barbuda	.ag
#Argentina	.ar
#Armenia	.am
#Aruba	.aw
#Australia	.au
#Austria	.at
#Azerbaijan	.az
#Bahamas	.bs
#Bahrain	.bh
#Bangladesh	.bd
#Barbados	.bb
#Basque Country	.eus
#Belarus	.by
#Belgium	.be
#Belize	.bz
#Benin	.bj
#Bermuda	.bm
#Bhutan	.bt
#Bolivia	.bo
#Bonaire	.bq
#Bosnia and Herzegovina	.ba
#Botswana	.bw
#Bouvet Island	.bv
#Brazil	.br
#British Indian Ocean Territory	.io
#British Virgin Islands	.vg
#Brunei	.bn
#Bulgaria	.bg
#Burkina Faso	.bf
#Myanmar	.mm
#Burundi	.bi
#Cambodia	.kh
#Cameroon	.cm
#Canada	.ca
#Cape Verde	.cv
#Catalonia	.cat
#Cayman Islands	.ky
#Central African Republic	.cf
#Chad	.td (stands for Tchad)
#Chile	.cl
#China	.cn
#Christmas Island	.cx
#Cocos (Keeling) Islands	.cc
#Colombia	.co
#Comoros	.km
#Democratic Republic of the Congo	.cd
#Congo	.cg
#Cook Islands	.ck
#Costa Rica	.cr
#Cote d'Ivoire (Ivory Coast)	.ci
#Croatia	.hr
#Cuba	.cu
#Cyprus	.cy
#Czech Republic	.cz
#Denmark	.dk
#Djibouti	.dj
#Dominica	.dm
#Dominican Republic	.do
#Timor-Leste	.tl
#Ecuador	.ec
#Egypt	.eg
#El Salvador	.sv
#Equatorial Guinea	.gq
#Eritrea	.er
#Estonia	.ee
#Ethiopia	.et
#European Union	.eu
#Falkland Islands	.fk
#Faeroe Islands	.fo
#Federated States of Micronesia	.fm
#Fiji	.fj
#Finland	.fi
#France	.fr
#French Guiana	.gf
#French Polynesia	.pf
#Gabon	.ga
#Galicia	.gal
#Gambia	.gm
#Gaza Strip	.ps
#Georgia	.ge
#Germany	.de
#Ghana	.gh
#Gibraltar	.gi
#Greece	.gr
#Greenland	.gl
#Grenada	.gd
#Guadeloupe	.gp
#Guam	.gu
#Guatemala	.gt
#Guernsey	.gg
#Guinea	.gn
#Guinea-Bissau	.gw
#Guyana	.gy
#Haiti	.ht
#Heard Island and McDonald Islands	.hm
#Honduras	.hn
#Hong Kong	.hk
#Hungary	.hu
#Iceland	.is
#India	.in
#Indonesia	.id
#Iran	.ir
#Iraq	.iq
#Ireland	.ie
#Isle of Man	.im
#Israel	.il
#Italy	.it
#Jamaica	.jm
#Japan	.jp
#Jersey	.je
#Jordan	.jo
#Kazakhstan	.kz
#Kenya	.ke
#Kiribati	.ki
#Kuwait	.kw
#Kyrgyzstan	.kg
#Laos	.la
#Latvia	.lv
#Lebanon	.lb
#Lesotho	.ls
#Liberia	.lr
#Libya	.ly
#Liechtenstein	.li
#Lithuania	.lt
#Luxembourg	.lu
#Macau	.mo
#Macedonia	.mk
#Madagascar	.mg
#Malawi	.mw
#Malaysia	.my
#Maldives	.mv
#Mali	.ml
#Malta	.mt
#Marshall Islands	.mh
#Martinique	.mq
#Mauritania	.mr
#Mauritius	.mu
#Mayotte	.yt
#Mexico	.mx
#Moldova	.md
#Monaco	.mc
#Mongolia	.mn
#Montenegro	.me
#Montserrat	.ms
#Morocco	.ma
#Mozambique	.mz
#Myanmar	.mm
#Namibia	.na
#Nauru	.nr
#Nepal	.np
#Netherlands	.nl
#New Caledonia	.nc
#New Zealand	.nz
#Nicaragua	.ni
#Niger	.ne
#Nigeria	.ng
#Niue	.nu
#Norfolk Island	.nf
#North Korea	.kp
#North Macedonia	.mk
#Northern Mariana Islands	.mp
#Norway	.no
#Oman	.om
#Pakistan	.pk
#Palau	.pw
#Palestine	.ps
#Panama	.pa
#Papua New Guinea	.pg
#Paraguay	.py
#Peru	.pe
#Philippines	.ph
#Pitcairn Islands	.pn
#Poland	.pl
#Portugal	.pt
#Puerto Rico	.pr
#Qatar	.qa
#Romania	.ro
#Russia	.ru
#Rwanda	.rw
#Reunion Island	.re
#Saint Helena	.sh
#Saint Kitts and Nevis	.kn
#Saint Lucia	.lc
#Saint-Pierre and Miquelon	.pm
#Saint Vincent and the Grenadines	.vc
#Samoa	.ws
#San Marino	.sm
#Sao Tome and Principe	.st
#Saudi Arabia	.sa
#Senegal	.sn
#Serbia	.rs
#Seychelles	.sc
#Sierra Leone	.sl
#Singapore	.sg
#Slovakia	.sk
#Slovenia	.si
#Solomon Islands	.sb
#Somalia	.so
#Somaliland	.so
#South Africa	.za
#South Korea	.kr
#South Sudan	.ss
#Spain	.es
#Sri Lanka	.lk
#Sudan	.sd
#Suriname	.sr
#Svalbard and Jan Mayen Islands	.sj
#Swaziland	.sz
#Sweden	.se
#Switzerland	.ch
#Syria	.sy
#Taiwan	.tw
#Tajikistan	.tj
#Tanzania	.tz
#Thailand	.th
#Togo	.tg
#Tokelau	.tk
#Tonga	.to
#Trinidad and Tobago	.tt
#Tunisia	.tn
#Turkey	.tr
#Turkmenistan	.tm
#Turks and Caicos Islands	.tc
#Tuvalu	.tv
#Uganda	.ug
#Ukraine	.ua
#United Arab Emirates	.ae
#United Kingdom	.gb
#United States	.us
#United States Virgin Islands	.vi
#Uruguay	.uy
#Uzbekistan	.uz
#Vanuatu	.vu
#Vatican City	.va
#Venezuela	.ve
#Vietnam	.vn
#Wallis and Futuna	.wf
#Western Sahara	.eh
#Yemen	.ye
#Zambia	.zm
#Zimbabwe	.zw
if [ ${#@} -lt 3 ]; then
echo "usage: ./tld.sh \"hmi+qt\" 4 India Ireland Canada .."
fi
arr=("$@")
for i in "${arr[@]:2}"; do
if egrep -i -q "^#\b$i\b"$'\t' tld.sh; then
 webcode=`egrep -i "^#\b$i\b"$'\t' tld.sh|cut -d$'\t' -f2|cut -d. -f2`
 python3 getconsole.py "$i" $webcode "$1" $2 
 filename=$1
 if [ `cat test.txt|wc -l` -gt 10 ]; then
  if [ $1 == "C++" -o $1 == "c++" ]; then
   filename="cpp"
  fi
  mv test.txt test_${webcode}_${filename}.txt
  echo "------------------------------- "
  echo "         test_${webcode}_${filename}.txt"
  echo "------------------------------- "
  echo $'\n'
  read -p "Press (y/n) to launch chainm.py ... " yorno
  if [ $yorno == "y" ]; then
   python3 chainm.py&
  fi
 else
  echo "test.txt line count : "`cat test.txt|wc -l`
 fi
else
echo "******Country $i not found*******"
fi
done
