<?
class UtilMc{
public function __construct(){
$level='.';
$headername="";
$subitem="";
foreach(split("\/",split("public_html\/?",ereg_replace("\/*$","",getcwd()))[1]) as $item){
 if(!empty($item)){ 
  if($level=='.')
   $headername=$item;
  elseif(empty($subitem))
   $subitem=$item;
  $level=$level."/..";
 }
}
?>
<html>
<head>
<title>Minh, Inc. Software development and Outsourcing <? echo "| ".${subitem}." ".${headername}." Bangalore India"; ?></title>
<link rel="stylesheet" type="text/css" href="<? echo $level ?>/css/main.css" media="all"/>
<link rel="stylesheet" type="text/css" href="<? echo $level ?>/css/agenda.css" media="all"/>
</head>
<body>
<?php include_once("analyticstracking.php") ?>
<a href="<? echo $level ?>/"><img src="<? echo $level ?>/image/topconLogo.png"/></a>
<br>
<div class="ddm">
 <ul class="drop">
  <li><a href="<? echo $level ?>/about/" style="<?php echo ($headername=='about'?'color:#f38502':'') ?>">About Minh</li>
  <li><div></div><a href="<? echo $level ?>/product/" style="<?php echo ($headername=='product'?'color:#f38502':'') ?>">Products</a>
   <ul>
    <li class="blank">" "</li>
    <li><a href="<? echo $level ?>/product/fs">Flight Simulator</a></li>
    <li><a href="<? echo $level ?>/product/mp">Media Player</a></li>
    <li><a href="<? echo $level ?>/product/ytd">YouTube Downloader</a></li>
    <li><a href="<? echo $level ?>/product/mas">Medical Annotation Software</a></li>
    <li><a href="<? echo $level ?>/product/3dv">3D Data Viewer</a></li>
    <li><a href="<? echo $level ?>/product/3dv">3D Data Viewer</a></li>
   </ul>
  </li>
  <li><div></div><a href="<? echo $level ?>/training/" style="<?php echo ($headername=='training'?'color:#f38502':'') ?>">Training</a>
   <ul>
    <li class="blank">" "</li>
    <li><div></div><a href="<? echo $level ?>/training/py">Python</a>
     <ul>
      <li><a class="leaf" href="<? echo $level ?>/training/py/advance-py-slides.php">Slides</a></li>
      <li><div></div><a href="<? echo $level ?>/research/">Articles</a>
       <ul>
        <li><a href="http://www.minhinc.com/research/accessingfilesinpython.txt">Accessing Files in Python</a></li>
       </ul>
      </li>
     </ul>
    </li>
    <li><div></div><a href="<? echo $level ?>/training/c">C</a>
     <ul>
      <li><a class="leaf" href="<? echo $level ?>/training/c/advance-c-slides.php">Slides</a></li>
      <li><div></div><a href="<? echo $level ?>/research/">Articles</a>
       <ul>
        <li><a href="http://www.ibm.com/developerworks/aix/library/au-aix-stack-tree-traversal">Stack Based Tree Traversal</a></li>
       </ul>
      </li>
     </ul>
    </li>
    <li><div></div><a href="<? echo $level ?>/training/cpp">C++</a>
     <ul>
      <li><a class="leaf" href="<? echo $level ?>/training/cpp/advance-cpp-slides.php">Slides</a></li>
      <li><div></div><a href="<? echo $level ?>/research/">Articles</a>
       <ul>
        <li><a href="http://www.codeguru.com/IoT/coding-analog-sensors-on-the-raspberry-pi3.html">Coding Analog Sensors On The Raspberry Pi3</a></li>
        <li><a href="http://www.codeguru.com/IoT/coding-sensors-on-the-rpi3.html">Coding Sensors On The Raspberry Pi3</a></li>
        <li><a href="http://www.codeguru.com/IoT/using-the-qt-2d-display-on-a-raspberry-pi3.html">The Qt 2d Display on a Raspberry pi3</a></li>
        <li><a href="http://www.codeguru.com/cpp/g-m/drawing-3d-opengl-graphics-on-google-maps.html">OpenGL drawing on Google Maps</a></li>
        <li><a href="http://www.codeguru.com/tools/commsoftfreecondit/qt-basics-the-chain-of-responsibility-pattern.html">Qt: Chain Of Responsibility</a></li>
        <li><a href="http://www.codeproject.com/Articles/869923/Class-Level-Generic-Logger">C++ Class Level Logger</a></li>
       </ul>
      </li>
     </ul>
    </li>
    <li><div></div><a href="<? echo $level ?>/training/qt">Qt</a>
     <ul>
      <li><a class="leaf" href="<? echo $level ?>/training/qt/advance-qt-slides.php">Slides</a></li>
      <li><div></div><a href="<? echo $level ?>/research/">Articles</a>
       <ul>
        <li><a href="http://www.codeguru.com/IoT/coding-analog-sensors-on-the-raspberry-pi3.html">Coding Analog Sensors On The Raspberry Pi3</a></li>
        <li><a href="http://www.codeguru.com/IoT/coding-sensors-on-the-rpi3.html">Coding Sensors On The Raspberry Pi3</a></li>
        <li><a href="http://www.codeguru.com/IoT/using-the-qt-2d-display-on-a-raspberry-pi3.html">The Qt 2d Display on a Raspberry pi3</a></li>
        <li><a href="http://www.codeguru.com/tools/commsoftfreecondit/qt-basics-the-chain-of-responsibility-pattern.html">Qt: Chain Of Responsibility</a></li>
        <li><a href="http://www.codeguru.com/cpp/g-m/drawing-3d-opengl-graphics-on-google-maps.html">OpenGL drawing on Google Maps</a></li>
       </ul>
      </li>
     </ul>
    </li>
    <li><div></div><a href="<? echo $level ?>/training/gl">OpenGL</a>
     <ul>
      <li><a class="leaf" href="<? echo $level ?>/training/gl/advance-gl-slides.php">Slides</a></li>
      <li><div></div><a href="<? echo $level ?>/research/">Articles</a>
       <ul>
        <li><a href="http://www.codeguru.com/cpp/g-m/drawing-3d-opengl-graphics-on-google-maps.htmlhp">OpenGL drawing on Google Maps</a></li>
       </ul>
      </li>
     </ul>
    </li>
    <li><div></div><a href="<? echo $level ?>/training/qml">Qml</a>
     <ul>
      <li><a class="leaf" href="<? echo $level ?>/training/qml/advance-qml-slides.php">Slides</a></li>
     </ul>
    </li>
    <li><div></div><a href="<? echo $level ?>/training/ldd">Linux Device Driver</a>
     <ul>
      <li><a class="leaf" href="<? echo $level ?>/training/ldd/advance-ldd-slides.php">Slides</a></li>
     </ul>
    </li>
    <li><div></div><a href="<? echo $level ?>/training/li">Linux Internals</a>
     <ul>
      <li><a class="leaf" href="<? echo $level ?>/training/li/advance-li-slides.php">Slides</a></li>
      <li><div></div><a href="<? echo $level ?>/research/">Articles</a>
       <ul>
        <li><a href="http://www.codeguru.com/IoT/coding-analog-sensors-on-the-raspberry-pi3.html">Coding Analog Sensors On The Raspberry Pi3</a></li>
        <li><a href="http://www.codeguru.com/IoT/coding-sensors-on-the-rpi3.html">Coding Sensors On The Raspberry Pi3</a></li>
        <li><a href="http://www.codeguru.com/IoT/raspberry-pi-3-hardware-and-system-software-reference.html">Raspberry Pi 3 Hardware And System Software Reference</a></li>
       </ul>
      </li>
     </ul>
    </li>
   </ul>
  </li>
  <li><div></div><a href="<? echo $level ?>/research/" style="<?php echo ($headername=='research'?'color:#f38502':'') ?>">Research</a>
   <ul>
    <li class="blank">" "</li>
    <li><a href="http://www.codeguru.com/IoT/coding-analog-sensors-on-the-raspberry-pi3.html">Coding Analog Sensors On The Raspberry Pi3</a></li>
    <li><a href="http://www.codeguru.com/IoT/coding-sensors-on-the-rpi3.html">Coding Sensors On The Raspberry Pi3</a></li>
    <li><a href="http://www.codeguru.com/IoT/raspberry-pi-3-hardware-and-system-software-reference.html">Raspberry Pi 3 Hardware And System Software Reference</a></li>
    <li><a href="http://www.codeguru.com/IoT/using-the-qt-2d-display-on-a-raspberry-pi3.html">The Qt 2d Display on a Raspberry pi3</a></li>
    <li><a href="http://www.developer.com/open/accessing-files-using-python.html">Accessing files using Python</a></li>
    <li><div></div><a href="http://www.codeguru.com/cpp/g-m/drawing-3d-opengl-graphics-on-google-maps.html">Qt OpenGL 3D drawing on Google Maps</a>
     <ul>
      <li><div></div><a href="<? echo $level ?>/product/">Product</a>
       <ul>
        <li><a href="<? echo $level ?>/product/fs">Flight Simulator</a></li>
       </ul>
      </li>
     </ul>
    </li>
    <li><a href="http://www.codeguru.com/tools/commsoftfreecondit/qt-basics-the-chain-of-responsibility-pattern.html">Qt Basic: The Chain Of Responsibility</a></li>
    <li><a href="http://www.codeproject.com/Articles/869923/Class-Level-Generic-Logger">C++ Class Level Generic Logger</a></li>
    <li><a href="http://sdjournal.org/download/sdj-open/">Design Patterns in Perl</a></li>
    <li><a href="http://www.ibm.com/developerworks/aix/library/au-aix-stack-tree-traversal">Stack Based BFS Traversal</a></li>
   </ul>
  </li>
  <li><div></div><a href="<? echo $level ?>/service/" style="<?php echo ($headername=='service'?'color:#f38502':'') ?>">Services</a>
   <ul>
    <li class="blank">" "</li>
    <li><a href="<? echo $level ?>/service/network">Network</a></li>
    <li><a href="<? echo $level ?>/service/multimedia">Multimedia</a></li>
    <li><a href="<? echo $level ?>/service/medicalsystem">Medical Systems</a></li>
   </ul>
  </li>
  <li><div></div><a href="../career/" style="<?php echo ($headername=='career'?'color:#f38502':'') ?>">Career</a>
   <ul>
    <li class="blank">" "</li>
    <li><a href="<? echo $level ?>/career/">Upload CV</a></li>
   </ul>
  </li>
  <li><div></div><a href="../about/" style="<?php echo ($headername=='help'?'color:#f38502':'') ?>">Help</a>
   <ul>
    <li class="blank">" "</li>
    <li><a href="<? echo $level ?>/about/">About Minh, Inc.</a></li>
    <li><a href="<? echo $level ?>/about/question">Ask a Programming Question</a></li>
    <li><a href="<? echo $level ?>/about/contact">Contact Us</a></li>
   </ul>
  </li>
 </ul>
</div>
<br>
 <ul class="domain">
  <li><a href="<? echo $level ?>/service/network">Networking</a></li>
  <li>|</li>
  <li><a href="<? echo $level ?>/service/multimedia">MultiMedia</a></li>
  <li>|</li>
  <li><a href="<? echo $level ?>/service/medicalsystem">Medical Systems</a></li>
 </ul>
<br>
<?
}
public function drawfooter(){
$headername="";
$subitem="";
$filename=getcwd();
foreach(split("\/",split("public_html\/?",ereg_replace("\/*$","",$filename))[1]) as $item){
if(empty($headername)){
 $headername=$item;
}elseif(empty($subitem) and !empty($headername)){
 $subitem=$item;
}
}
if($headername=='training' or $headername=='product' or $headername =='service' or $headername=='career'){
  $this->drawtrainingleft($headername,$subitem);
}
?>
<div class="footer">
 <hr>
 <ul class="fl">
  <li><p class="bold" style="margin:0px;padding:0px;">Minh, Inc.</p></li>
  <li><p>#85, 5th Main, P&T<br>
   SanjayNagar, Bangalore<br>
   Karnataka, India 560094<br>
   Ph - +91 9483160610<br></p>
  </li>
 </ul>
 <ul class="menu">
  <li class="top"><a href="<? echo $level ?>/product/">Product</a>
   <ul>
    <li><hr class="product" style="<?php echo ($headername=='product'?'background-color:#f38502':'') ?>"></li>
    <li><a href="<? echo $level ?>/product/ytd" <? echo ($subitem=='ytd'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Youtube Downloader</a><li>
    <li><a href="<? echo $level ?>/product/mp" <? echo ($subitem=='mp'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Media Player</a><li>
    <li><a href="<? echo $level ?>/product/fs" <? echo ($subitem=='fs'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Flight Simulator</a><li>
    <li><a href="<? echo $level ?>/product/mas" <? echo ($subitem=='mas'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Medical Annotation Software</a><li>
    <li><a href="<? echo $level ?>/product/3dv" <? echo ($subitem=='3dv'?'style="font-weight:bold;color:#aa4400;"':'') ?>>3D Data Viewer</a><li>
   </ul>
  </li>
  <li class="top"><a href="<? echo $level ?>/training/">Training</a>
   <ul>
    <li><hr class="training" style="<?php echo ($headername=='training'?'background-color:#f38502':'') ?>"></li>
    <li><a href="<? echo $level ?>/training/py" <? echo ($subitem=='py'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Python</a></li>
    <li><a href="<? echo $level ?>/training/c"  <? echo ($subitem=='c'?'style="font-weight:bold;color:#aa4400;"':'') ?>>C</a></li>
    <li><a href="<? echo $level ?>/training/qt" <? echo ($subitem=='qt'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Qt</a></li>
    <li><a href="<? echo $level ?>/training/qt" <? echo ($subitem=='qml'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Qml</a></li>
    <li><a href="<? echo $level ?>/training/cpp" <? echo ($subitem=='cpp'?'style="font-weight:bold;color:#aa4400;"':'') ?>>C++</a></li>
    <li><a href="<? echo $level ?>/training/gl" <? echo ($subitem=='gl'?'style="font-weight:bold;color:#aa4400;"':'') ?>>OpenGL</a></li>
    <li><a href="<? echo $level ?>/training/ldd" <? echo ($subitem=='ldd'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Linux Device Driver</a></li>
    <li><a href="<? echo $level ?>/training/li" <? echo ($subitem=='li'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Linux Internals</a></li>
   </ul>
  </li>
  <li class="top"><a href="<? echo $level ?>/research/">Research</a>
   <ul>
    <li><hr class="research" style="<?php echo ($headername=='research'?'background-color:#f38502':'') ?>"></li>
   </ul>
  </li>
  <li class="top"><a href="<? echo $level ?>/services/">Services</a>
   <ul>
    <li><hr class="services" style="<?php echo ($headername=='service'?'background-color:#f38502':'') ?>"></li>
    <li><a href="<? echo $level ?>/service/network" <? echo ($subitem=='network'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Networking</a><li>
    <li><a href="<? echo $level ?>/service/multimedia" <? echo ($subitem=='multimedia'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Multimedia</a></li>
    <li><a href="<? echo $level ?>/service/medicalsystem" <? echo ($subitem=='medicalsystem'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Medical Systems</a></li>
   </ul>
  </li>
  <li class="top"><a href="<? echo $level ?>/career/">Career</a>
   <ul>
    <li><hr class="career" style="<?php echo ($headername=='career'?'background-color:#f38502':'') ?>"></li>
   </ul>
  </li>
  <li class="top"><a href="<? echo $level ?>/about/">Help</a>
   <ul>
    <li><hr class="help" style="<?php echo ($headername=='about'?'background-color:#f38502':'') ?>"></li>
    <li><a href="<? echo $level ?>/about/question" <? echo ($subitem=='question'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Ask a programming question</a></li>
    <li><a href="<? echo $level ?>/about/contact" <? echo ($subitem=='contact'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Contact Us</a></li>
   </ul>
  </li>
 </ul>
 <ul class="fr">
  <li><p>&copy Minh Corporation 2015-2017</p></li>
  <li class="img"><a href="https://github.com/minhinc/"><img src="<? echo $level ?>/image/githubs.png"/></a><a href="https://linkedin.com/in/pravinkumarsinha/"><img src="<? echo $level ?>/image/linkedins.png"/></a><a href="https://facebook.com/minhinc/"><img src="<? echo $level ?>/image/fbs.png"/></a></li>
 </ul>
</div>
</body>
</html>
<?
}
public function drawtrainingleft($headername,$tech){
$pdir='.';
if(!empty($tech)){
$pdir='..';
}
?>
<div class="downloadleft">
<ul class="tablist">
<a href="<? echo $pdir.'/'.$headername; ?>"><li class="header"><p><? echo ucfirst($headername); ?></p></li></a>

<? if ($headername == 'training'){
if($tech == 'py'){ ?>
<li class="current"><p class="padtop">Python Training</p></li>
<? }else{ ?>
<a href="<? echo $pdir.'/py'; ?>"><li class="light"><p>Python Training</p></li></a>
<? } ?>

<? if($tech == 'cpp'){ ?>
<li class="current"><p class="padtop">C++ Training</p></li>
<? }else{ ?>
<a href="<? echo $pdir.'/cpp'; ?>"><li class="dark"><p>C++ Training</p></li></a>
<? } ?>

<? if($tech == 'qt'){ ?>
<li class="current"><p class="padtop">Qt Training</p></li>
<? }else{ ?>
<a href="<? echo $pdir.'/qt'; ?>"><li class="light"><p>Qt Training</p></li></a>
<? } ?>

<? if($tech == 'qml'){ ?>
<li class="current"><p class="padtop">Qml Training</p></li>
<? }else{ ?>
<a href="<? echo $pdir.'/qml'; ?>"><li class="light"><p>Qml Training</p></li></a>
<? } ?>

<? if($tech == 'c'){ ?>
<li class="current"><p class="padtop">C Training</p></li>
<? }else{ ?>
<a href="<? echo $pdir.'/c'; ?>"><li class="dark"><p>C Training</p></li></a>
<? } ?>

<? if($tech == 'gl'){ ?>
<li class="current"><p class="padtop">OpenGL Training</p></li>
<? }else{ ?>
<a href="<? echo $pdir.'/gl'; ?>"><li class="light"><p>OpenGL Training</p></li></a>
<? } ?>

<? if($tech == 'ldd'){ ?>
<li class="current"><p class="padtop">Linux Device Driver Training</p></li>
<? }else{ ?>
<a href="<? echo $pdir.'/ldd'; ?>"><li class="dark"><p>Linux Device Driver Training</p></li></a>
<? } ?>

<? if($tech == 'li'){ ?>
<li class="current"><p class="padtop">Linux Internals Training</p></li>
<? }else{ ?>
<a href="<? echo $pdir.'/li'; ?>"><li class="light"><p>Linux Internals Training</p></li></a>
<? } ?>

<? }elseif ($headername=='product'){
if($tech == 'ytd'){ ?>
<li class="current"><p>YouTube Downloader built-in Player</p></li>
<? }else{ ?>
<a href="<? echo $pdir.'/ytd'; ?>"><li class="light"><p>YouTube Downloader built-in Player</p></li></a>
<? } ?>

<? if($tech == 'mp'){ ?>
<li class="current"><p>Media Player</p></li>
<? }else{ ?>
<a href="<? echo $pdir.'/mp'; ?>"><li class="dark"><p>Media Player</p></li></a>
<? } ?>

<? if($tech == 'fs'){ ?>
<li class="current"><p>QtGL Flight Simulator</p></li>
<? }else{ ?>
<a href="<? echo $pdir.'/fs'; ?>"><li class="light"><p>QtGL Flight Simulator</p></li></a>
<? } ?>

<? if($tech == 'mas'){ ?>
<li class="current"><p>Medical Annotation Software</p></li>
<? }else{ ?>
<a href="<? echo $pdir.'/mas'; ?>"><li class="dark"><p>Medical Annotation Software</p></li></a>
<? } ?>

<? if($tech == '3dv'){ ?>
<li class="current"><p>3D Data Viewer</p></li>
<? }else{ ?>
<a href="<? echo $pdir.'/3dv'; ?>"><li class="light"><p>3D Data Viewer</p></li></a>
<? } ?>

<? }elseif ($headername=='service'){
if($tech == 'network'){ ?>
<li class="current"><p>Network</p></li>
<? }else{ ?>
<a href="<? echo $pdir.'/network'; ?>"><li class="light"><p>Network</p></li></a>
<? } ?>

<? if($tech == 'multimedia'){ ?>
<li class="current"><p>Multimedia</p></li>
<? }else{ ?>
<a href="<? echo $pdir.'/multimedia'; ?>"><li class="dark"><p>Multimedia</p></li></a>
<? } ?>

<? if($tech == 'medicalsystem'){ ?>
<li class="current"><p>Medical Systems</p></li>
<? }else{ ?>
<a href="<? echo $pdir.'/medicalsystem'; ?>"><li class="light"><p>Medical Systems</p></li></a>
<? } ?>

<? }elseif ($headername=='career'){
if($tech == 'cv'){ ?>
<li class="current"><p>Carriculum Vitae</p></li>
<? }else{ ?>
<a href="<? echo $pdir.'/'; ?>"><li class="light"><p>Carriculum Vitae</p></li></a>
<? } ?>
<? } ?>

</ul>
</div>
<?
}
public function drawmain($platform){
?>
<div class="leftpan">
 <a href="./product/home.html"><img src="./image/mytda.png"/></a>
 <div class="research">
  <ul class="research">
   <a href="./research/home.html"><li class="header"><p>Research</p></li></a>
   <a href="http://www.codeguru.com/IoT/coding-analog-sensors-on-the-raspberry-pi3.html"><li class="light"><p class="t">Coding Analog Sensors On The Raspberry Pi3</p><p class="b">codeguru.com,Sep 2017</p><img src="./image/dv.png"/></li></a>
   <a href="http://www.codeguru.com/IoT/coding-sensors-on-the-rpi3.html"><li class="light"><p class="t">Coding Sensors On The Raspberry Pi3</p><p class="b">codeguru.com,Sep 2017</p><img src="./image/dv.png"/></li></a>
   <a href="http://www.codeguru.com/IoT/raspberry-pi-3-hardware-and-system-software-reference.html"><li class="light"><p class="t">Raspberry Pi 3 Hardware And System Software Reference</p><p class="b">codeguru.com,Sep 2017</p><img src="./image/dv.png"/></li></a>
   <a href="http://www.codeguru.com/IoT/using-the-qt-2d-display-on-a-raspberry-pi3.html"><li class="light"><p class="t">The Qt 2d Display on a Raspberry pi3</p><p class="b">codeguru.com,Sep 2017</p><img src="./image/dv.png"/></li></a>
   <a href="http://www.developer.com/open/accessing-files-using-python.html"><li class="dark"><p class="t">Accessing Files Using Python</p><p class="b">developer.com,Jan 2017</p><img src="./image/dev.png"/></li></a>
   <a href="http://www.codeguru.com/cpp/g-m/drawing-3d-opengl-graphics-on-google-maps.html"><li class="light"><p class="t">Qt OpenGL 3D drawing on Google Maps</p><p class="b">codeguru.com,May 2016</p><img src="./image/dv.png"/></li></a>
   <a href="http://www.codeguru.com/tools/commsoftfreecondit/qt-basics-the-chain-of-responsibility-pattern.html"><li class="dark"><p class="t">Qt Basic: The Chain of Responsiblity Pattern</p><p class="b">codeguru.com,Nov 2015</p><img src="./image/dv.png"/></li></a>
   <a href="http://www.codeproject.com/Articles/869923/Class-Level-Generic-Logger"><li class="light"><p class="t">C++ Class Level Generic Logger</p><p class="b">codeproject.com,Jan 2015</p><img src="./image/cp.png"/></li></a>
   <a href="./research/SDJ_Open_2014.pdf"><li class="dark"><p class="t">Design Patterns in Perl</p><p class="b">SDJ,Nov 2014</p><img src="./image/sdj.png"/></li></a>
   <a href="http://www.ibm.com/developerworks/aix/library/au-aix-stack-tree-traversal"><li class="light"><p class="t">Stack Based Breadth First Tree Traversal</p><p class="b">IBM dw,Mar 2013</p><img src="./image/dw.png"/></li></a>
  </ul>
  </div>
  <div class="product">
  <ul class="research">
   <a href="./product/home.html"><li class="header"><p>Product</p></li></a>
   <a href="./product/nfs.html"><li class="light"><p class="t">Qt Based 3D OpenGL Flight Simulator on Google Maps</p><p class="b">Aug 2016</p><img src="./image/nz.png"/></li></a>
   <a href="./product/gmp.html"><li class="dark"><p class="t">Qt Based Media Player.</p><p class="b">Aug 2016</p><img src="./image/gmp.png"/></li></a>
   <a href="./product/gfd.html"><li class="light"><p class="t">Qt Based YouTube Downloader</p><p class="b">Aug 2016</p><img src="./image/gfd.png"/></li></a>
   <a href="./product/pas.html"><li class="dark"><p class="t">Medical Annotation Software</p><p class="b red">Upcoming</p></li></a>
   <a href="./product/dv.html"><li class="light"><p class="t">PythonGL based 3D data viewer</p><p class="b red">Upcoming</p></li></a>
  </ul>
  </div>
</div>

<div class="rightpan">
 <ul class="events">
  <li class="header"><p>Upcoming Events</p></li>
  <li class="light"><p class="t">Annotation Tool</p><p class="b"></p></li>
  <li class="dark"><p class="t">Building Qt on Raspberry Pi</p><p class="b"></p></li>
  <li class="light"><p class="t">WayLand Window Manager support on Embedded device</p><p class="b"></p></li>
  <li class="dark"><p class="t">Python 3D openGL based graphics</p><p class="b"></p></li>
 </ul>
 <ul class="next">
  <a href="./training.home.html"><li class="header"><p>Training</p></li></a>
  <li class="light"><a class="ls" href="./training/py/advance-py-slides.php">Slides</a><a href="./training/py"><img class="l" src="./image/python.png"/></a><a class="rs" href="./training/cpp/advance-cpp-slides.php">Slides</a><a href="./training/cpp"><img class="r" src="./image/cpp.png"/></a></li>
  <li class="dark"><a class="ls" href="./training/qt/advance-qt-slides.php">Slides</a><a href="./training/qt"><img class="l" src="./image/qt.png"/></a><a class="rs" href="./training/c/advance-c-slides.php">Slides</a><a href="./training/c"><img class="r" src="./image/c.png"/></a></li>
  <li class="light"><a class="ls" href="./training/gl/advance-gl-slides.php">Slides</a><a href="./training/gl"><img class="l" src="./image/opengl.png"/></a><a class="rs" href="./training/ldd/advance-ldd-slides.php">Slides</a><a href="./training/ldd"><img class="r" src="./image/ldd.png"/></a></li>
  <li class="dark"><a class="ls" href="./training/li/advance-li-slides.php">Slides</a><a href="./training/li"><img class="l" src="./image/li.png"/></a><a class="rs" href="./training/qml/advance-qml-slides.php">Slides</a><a href="./training/qml"><img class="r" src="./image/qml.png"/></a></li>
 </ul>
</div>
<?
$this->drawfooter();
}
}
?>
