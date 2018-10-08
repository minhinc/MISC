<?
class Utilpdfc{
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
<?
}
public function drawfooter($filename){
$headername="";
$subitem="";
foreach(split("\/",split("public_html\/?",ereg_replace("\/*$","",$filename))[1]) as $item){
 if(empty($headername)){
  $headername=$item;
 }elseif(empty($subitem) and !preg_grep("/[.]php$/",[$item])){
  $subitem=$item;
 }elseif(!empty($subitem) and preg_grep("/index[.]php$/",[$item])){
  if($headername=='training'){
   $this->drawtrainingleft($subitem);
  }elseif($headername=='product'){
   $this->drawproductleft($subitem);
  }
 }
}
?>
<div class="footer">
 <hr>
 <ul class="fl">
  <li><p class="bold">Minh, Inc.</p></li>
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
    <li><a href="<? echo $level ?>/product/gfd">Youtube Downloader</a><li>
    <li><a href="<? echo $level ?>/product/gmp">Media Player</a><li>
    <li><a href="<? echo $level ?>/product/nfs">Flight Simulator</a><li>
    <li><a href="<? echo $level ?>/product/mas">Medical Annotation Software</a><li>
    <li><a href="<? echo $level ?>/product/dv">3D Data Viewer</a><li>
   </ul>
  </li>
  <li class="top"><a href="<? echo $level ?>/training/">Training</a>
   <ul>
    <li><hr class="training" style="<?php echo ($headername=='training'?'background-color:#f38502':'') ?>"></li>
    <li><a href="<? echo $level ?>/training/py" <? echo ($subitem=='py'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Python</a></li>
    <li><a href="<? echo $level ?>/training/c"  <? echo ($subitem=='c'?'style="font-weight:bold;color:#aa4400;"':'') ?>>C</a></li>
    <li><a href="<? echo $level ?>/training/qt" <? echo ($subitem=='qt'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Qt/Qml</a></li>
    <li><a href="<? echo $level ?>/training/cpp" <? echo ($subitem=='cpp'?'style="font-weight:bold;color:#aa4400;"':'') ?>>C++</a></li>
    <li><a href="<? echo $level ?>/training/opengl" <? echo ($subitem=='gl'?'style="font-weight:bold;color:#aa4400;"':'') ?>>OpenGL</a></li>
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
    <li><a href="<? echo $level ?>/service/network">Networking</a><li>
    <li><a href="<? echo $level ?>/service/multimedia">Multimedia</a></li>
    <li><a href="<? echo $level ?>/service/medicalsystem">Medical Systems</a></li>
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
    <li><a href="<? echo $level ?>/about/question">Ask a programming question</a></li>
    <li><a href="<? echo $level ?>/about/contact">Contact Us</a></li>
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
public function drawtrainingleft($tech){
echo "tech:$tech";
?>
<div class="downloadleft">
<ul class="tablist">
<a href="../training/"><li class="header"><p>Training</p></li></a>

<? if($tech == 'py'){ ?>
<li class="current"><p class="padtop">Linux Internals Training</p></li>
<? }else{ ?>
<a href="../py"><li class="light"><p>Python Training</p></li></a>
<? } ?>

<? if($tech == 'cpp'){ ?>
<li class="current"><p class="padtop">C++ Training</p></li>
<? }else{ ?>
<a href="../cpp"><li class="dark"><p>C++ Training</p></li></a>
<? } ?>

<? if($tech == 'qt'){ ?>
<li class="current"><p class="padtop">Qt/Qml Training</p></li>
<? }else{ ?>
<a href="../qt"><li class="light"><p>Qt/Qml Training</p></li></a>
<? } ?>

<? if($tech == 'c'){ ?>
<li class="current"><p class="padtop">C Training</p></li>
<? }else{ ?>
<a href="../c"><li class="dark"><p>C Training</p></li></a>
<? } ?>

<? if($tech == 'gl'){ ?>
<li class="current"><p class="padtop">OpenGL Training</p></li>
<? }else{ ?>
<a href="../opengl"><li class="light"><p>OpenGL Training</p></li></a>
<? } ?>

<? if($tech == 'ldd'){ ?>
<li class="current"><p class="padtop">Linux Device Driver Training</p></li>
<? }else{ ?>
<a href="../ldd"><li class="dark"><p>Linux Device Driver Training</p></li></a>
<? } ?>

<? if($tech == 'li'){ ?>
<li class="current"><p class="padtop">Linux Internals Training</p></li>
<? }else{ ?>
<a href="../li"><li class="light"><p>Linux Internals Training</p></li></a>
<? } ?>
</ul>
</div>
<?
}
public function drawproductleft($tech){
?>
<div class="downloadleft">
<ul class="tablist">
<a href="../"><li class="header"><p>Product</p></li></a>

<? if($tech == 'gfd'){ ?>
<li class="current"><p>YouTube Downloader built-in Player</p></li>
<? }else{ ?>
<a href="../ytd"><li class="light"><p>YouTube Downloader built-in Player</p></li></a>
<? } ?>

<? if($tech == 'gmp'){ ?>
<li class="current"><p>Media Player</p></li>
<? }else{ ?>
<a href="../mp"><li class="dark"><p>Media Player</p></li></a>
<? } ?>

<? if($tech == 'nfs'){ ?>
<li class="current"><p>QtGL Flight Simulator</p></li>
<? }else{ ?>
<a href="../fs"><li class="light"><p>QtGL Flight Simulator</p></li></a>
<? } ?>
</ul>
</div>
<?
}
}
?>
