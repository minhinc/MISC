<?
require_once('Utilbm.php');
class Utilc extends Utilbc{
public function drawscript(){
 if (strlen(strstr($_SERVER['HTTP_USER_AGENT'],'Firefox')) > 0)
  echo file_get_contents($this->script.$this->chap.'_f.txt');
 else
  echo file_get_contents($this->script.$this->chap.'.txt');
}
public function draw(){
 require_once($this->json['pattern'].'.php');
 draw($this);
}

public function drawheader(){
$json['title']='';
if (!empty($this->subitem)) $json=json_decode(mysqli_fetch_row($this->db->get('headername','content','name',$this->subitem))[0],true);
elseif(!empty($this->headername)) $json=json_decode(mysqli_fetch_row($this->db->get('headername','content','name',$this->headername))[0],true);
?>
<html>
<head>
<meta charset="UTF-8">
<meta name="description" content="Training and Research Tutorials">
<meta name="keywords" content="HTML, CSS, JavaScript, Python, Machine Learning, Artificial Intelligence, ML, AI">
<meta name="author" content="Minh Inc">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script data-ad-client="ca-pub-8488699542117607" async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<script src="https://www.google.com/recaptcha/api.js" async defer></script>
<?
echo '<link rel="icon" type="image/png" href="'.$this->level.'/image/favicon-16x16.png" sizes="16x16">
      <link rel="icon" type="image/png" href="'.$this->level.'/image/favicon-32x32.png" sizes="32x32">
      <link rel="icon" type="image/png" href="'.$this->level.'/image/favicon-48x48.png" sizes="48x48">';
if (empty($this->headername)){
echo '<title>Minh, Inc. Software development and Outsourcing Bangalore India</title>';
}else{
echo '<title>'.$json['title'].' | Minh, Inc. Bangalore India</title>';
}
?>
<link rel="stylesheet" type="text/css" href="<? echo $this->level ?>/css/main.css" media="all"/>
<link rel="stylesheet" type="text/css" href="<? echo $this->level ?>/css/agenda.css" media="all"/>
</head>
<body>
<?php include_once('analyticstracking.php') ?>
<a href="<? echo $this->level ?>/"><img src="<? echo $this->level ?>/image/topconLogo.png"/></a>
<br>
<div class="ddm">
 <ul class="drop">
  <li><a href="<? echo $this->level ?>/about/" style="<?php echo ($this->headername=='about' && empty($this->subitem)?'color:#f38502':'') ?>">About Minh</li>
  <li><div></div><a href="<? echo $this->level ?>/product/" style="<?php echo ($this->headername=='product'?'color:#f38502':'') ?>">Products</a>
   <ul>
    <li class="blank">" "</li>
    <li><a href="<? echo $this->level ?>/product/fs">Flight Simulator</a></li>
    <li><a href="<? echo $this->level ?>/product/mp">Media Player</a></li>
    <li><a href="<? echo $this->level ?>/product/ytd">YouTube Downloader</a></li>
    <li><a href="<? echo $this->level ?>/product/mas">Medical Annotation Software</a></li>
    <li><a href="<? echo $this->level ?>/product/3dv">3D Data Viewer</a></li>
   </ul>
  </li>
  <li><div></div><a href="<? echo $this->level ?>/training/" style="<?php echo ($this->headername=='training'?'color:#f38502':'') ?>">Training</a>
   <ul>
    <li class="blank">" "</li>
    <li><div></div><a href="<? echo $this->level ?>/training/py">Python</a>
     <ul>
      <li><a class="leaf" href="<? echo $this->level ?>/training/py/advance-py-slides.php">Slides</a></li>
      <li><div></div><a href="<? echo $this->level ?>/research/">Articles</a>
       <ul>
        <li><a href="http://www.developer.com/open/accessing-files-using-python.html">Accessing Files in Python</a></li>
        <li><a href="http://minhinc.42web.io/research/rectanglepacking.pdf">Rectangle packing using Python</a></li>
       </ul>
      </li>
     </ul>
    </li>
    <li><div></div><a href="<? echo $this->level ?>/training/c">C</a>
     <ul>
      <li><a class="leaf" href="<? echo $this->level ?>/training/c/advance-c-slides.php">Slides</a></li>
      <li><div></div><a href="<? echo $this->level ?>/research/">Articles</a>
       <ul>
        <li><a href="http://www.ibm.com/developerworks/aix/library/au-aix-stack-tree-traversal">Stack Based Tree Traversal</a></li>
       </ul>
      </li>
     </ul>
    </li>
    <li><div></div><a href="<? echo $this->level ?>/training/cpp">C++</a>
     <ul>
      <li><a class="leaf" href="<? echo $this->level ?>/training/cpp/advance-cpp-slides.php">Slides</a></li>
      <li><div></div><a href="<? echo $this->level ?>/research/">Articles</a>
       <ul>
        <li><a href="http://www.codeguru.com/IoT/coding-analog-sensors-on-the-raspberry-pi3.html">Coding Analog Sensors On The Raspberry Pi3</a></li>
        <li><a href="http://www.codeguru.com/IoT/coding-sensors-on-the-rpi3.html">Coding Sensors On The Raspberry Pi3</a></li>
        <li><a href="http://www.codeguru.com/IoT/using-the-qt-2d-display-on-a-raspberry-pi3.html">The Qt 2d Display on a Raspberry pi3</a></li>
        <li><a href="http://www.codeguru.com/cpp/g-m/drawing-3d-opengl-graphics-on-google-maps.html">OpenGL drawing on Google Maps</a></li>
        <li><a href="http://www.codeguru.com/tools/commsoftfreecondit/qt-basics-the-chain-of-responsibility-pattern.html">Qt: Chain Of Responsibility</a></li>
        <li><a href="http://www.codeproject.com/Articles/869923/Class-Level-Generic-Logger">C++ Class Level Logger</a></li>
        <li><a href="https://www.eeweb.com/innovative-methods-in-design-patterns-with-c">Innovative Methods in Design Patterns with C++</a></li>
       </ul>
      </li>
     </ul>
    </li>
    <li><div></div><a href="<? echo $this->level ?>/training/qt">Qt</a>
     <ul>
      <li><a class="leaf" href="<? echo $this->level ?>/training/qt/advance-qt-slides.php">Slides</a></li>
      <li><div></div><a href="<? echo $this->level ?>/research/">Articles</a>
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
    <li><div></div><a href="<? echo $this->level ?>/training/gl">OpenGL</a>
     <ul>
      <li><a class="leaf" href="<? echo $this->level ?>/training/gl/advance-gl-slides.php">Slides</a></li>
      <li><div></div><a href="<? echo $this->level ?>/research/">Articles</a>
       <ul>
        <li><a href="http://www.codeguru.com/cpp/g-m/drawing-3d-opengl-graphics-on-google-maps.htmlhp">OpenGL drawing on Google Maps</a></li>
       </ul>
      </li>
     </ul>
    </li>
    <li><div></div><a href="<? echo $this->level ?>/training/qml">Qml</a>
     <ul>
      <li><a class="leaf" href="<? echo $this->level ?>/training/qml/advance-qml-slides.php">Slides</a></li>
     </ul>
    </li>
    <li><div></div><a href="<? echo $this->level ?>/training/ldd">Linux Device Driver</a>
     <ul>
      <li><a class="leaf" href="<? echo $this->level ?>/training/ldd/advance-ldd-slides.php">Slides</a></li>
     </ul>
    </li>
    <li><div></div><a href="<? echo $this->level ?>/training/li">Linux Internals</a>
     <ul>
      <li><a class="leaf" href="<? echo $this->level ?>/training/li/advance-li-slides.php">Slides</a></li>
      <li><div></div><a href="<? echo $this->level ?>/research/">Articles</a>
       <ul>
        <li><a href="http://www.codeguru.com/IoT/coding-analog-sensors-on-the-raspberry-pi3.html">Coding Analog Sensors On The Raspberry Pi3</a></li>
        <li><a href="http://www.codeguru.com/IoT/coding-sensors-on-the-rpi3.html">Coding Sensors On The Raspberry Pi3</a></li>
        <li><a href="http://www.codeguru.com/IoT/raspberry-pi-3-hardware-and-system-software-reference.html">Raspberry Pi 3 Hardware And System Software Reference</a></li>
       </ul>
      </li>
     </ul>
    </li>
    <li><div></div><a href="<? echo $this->level ?>/training/dp">GOF Design Patterns</a>
     <ul>
      <li><a class="leaf" href="<? echo $this->level ?>/training/dp/advance-dp-slides.php">Slides</a></li>
      <li><div></div><a href="<? echo $this->level ?>/research/">Articles</a>
       <ul>
        <li><a href="http://www.minhinc.42web.io/research/SDJ_Open_2014.pdf">Design Patterns in Perl</a></li>
       </ul>
      </li>
     </ul>
    </li>
   </ul>
  </li>
  <li><div></div><a href="<? echo $this->level ?>/research/" style="<?php echo ($this->headername=='research'?'color:#f38502':'') ?>">Research</a>
   <ul>
    <li class="blank">" "</li>
    <li><a href="https://www.eeweb.com/innovative-methods-in-design-patterns-with-c">Innovative Methods in Design Patterns with C++</a></li>
    <li><a href="http://minhinc.42web.io/research/rectanglepacking.pdf">Rectangle Packing using Python</a></li>
    <li><a href="https://www.codeproject.com/Articles/1271791/GUI-Modeling-in-Perl-Tk-Using-Composite-Design-Pat">GUI Modeling in Perl/Tk Using Composite Design Pattern</a></li>
    <li><a href="http://www.codeguru.com/IoT/coding-analog-sensors-on-the-raspberry-pi3.html">Coding Analog Sensors On The Raspberry Pi3</a></li>
    <li><a href="http://www.codeguru.com/IoT/coding-sensors-on-the-rpi3.html">Coding Sensors On The Raspberry Pi3</a></li>
    <li><a href="http://www.codeguru.com/IoT/raspberry-pi-3-hardware-and-system-software-reference.html">Raspberry Pi 3 Hardware And System Software Reference</a></li>
    <li><a href="http://www.codeguru.com/IoT/using-the-qt-2d-display-on-a-raspberry-pi3.html">The Qt 2d Display on a Raspberry pi3</a></li>
    <li><a href="http://www.developer.com/open/accessing-files-using-python.html">Accessing files using Python</a></li>
    <li><div></div><a href="http://www.codeguru.com/cpp/g-m/drawing-3d-opengl-graphics-on-google-maps.html">Qt OpenGL 3D drawing on Google Maps</a>
     <ul>
      <li><div></div><a href="<? echo $this->level ?>/product/">Product</a>
       <ul>
        <li><a href="<? echo $this->level ?>/product/fs">Flight Simulator</a></li>
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
  <li><div></div><a href="<? echo $this->level ?>/service/" style="<?php echo ($this->headername=='service'?'color:#f38502':'') ?>">Services</a>
   <ul>
    <li class="blank">" "</li>
    <li><a href="<? echo $this->level ?>/service/network">Network</a></li>
    <li><a href="<? echo $this->level ?>/service/multimedia">Multimedia</a></li>
    <li><a href="<? echo $this->level ?>/service/medicalsystem">Medical Systems</a></li>
   </ul>
  </li>
  <li><div></div><a href="<? echo $this->level ?>/career/" style="<?php echo ($this->headername=='career'?'color:#f38502':'') ?>">Career</a>
   <ul>
    <li class="blank">" "</li>
    <li><a href="<? echo $this->level ?>/career/">Upload CV</a></li>
   </ul>
  </li>
  <li><div></div><a href="<? echo $this->level ?>/about/" style="<?php echo ($this->headername=='about'?'color:#f38502':'') ?>">Help</a>
   <ul>
    <li class="blank">" "</li>
    <li><a href="<? echo $this->level ?>/about/">About Minh, Inc.</a></li>
    <li><a href="<? echo $this->level ?>/online" <? echo ($this->subitem=='online'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Online Training</a></li>
    <li><a href="<? echo $this->level ?>/about/question">Ask a Programming Question</a></li>
    <li><a href="<? echo $this->level ?>/about/contact">Contact Us</a></li>
   </ul>
  </li>
 </ul>
</div>
<br>
 <ul class="domain">
  <li><a href="<? echo $this->level ?>/service/network" <? echo ($this->subitem=='networking'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Networking</a></li>
  <li>|</li>
  <li><a href="<? echo $this->level ?>/service/multimedia" <? echo ($this->subitem=='multimedia'?'style="font-weight:bold;color:#aa4400;"':'') ?>>MultiMedia</a></li>
  <li>|</li>
  <li><a href="<? echo $this->level ?>/service/medicalsystem" <? echo ($this->subitem=='medicalsystem'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Medical Systems</a></li>
  <li>|</li>
  <li><a href="<? echo $this->level ?>/online" <? echo ($this->subitem=='online'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Online Training</a></li>
 </ul>
<br>
<?
/* Top Advertisement */
$json=json_decode(mysqli_fetch_row($this->db->get('headername','content','name','main'))[0],true);
if (!empty($json['comingtraining']) && $this->headername != "about" && $this->subitem != "online"){
echo '<div style="width:70%;height:60px;margin:10px auto;background-color:#0707a2"><pre style="float:left;padding-left:5%;line-height:60px;color:#ffffff;font-family:mytwcenmt;font-size:22px;">';
echo $json['comingtraining'];
echo '</pre><a href="http://www.minhinc.42web.io/online" style="float:right;margin:10px 5%;padding:0px 5px;border-radius:5px;display:block;background-color:#53616e;line-height:40px;font-size:20px;color:#ffffff";font-family:arial, helvetica, sans;>...Know More</a></div><div style="clear:both"></div>';
}

}
public function drawfooter(){
/*$this->headername="";
$this->subitem="";
foreach(preg_split("/\//",preg_split("/public_html\/?/",preg_replace("/\/*$/","",getcwd()))[1]) as $item){
if(empty($this->headername)){
 $this->headername=$item;
}elseif(empty($this->subitem) and !empty($this->headername)){
 $this->subitem=$item;
}
}*/
?>
<div class="footer">
 <hr>
 <ul class="fl">
  <li><p class="bold" style="margin:0px;padding:0px;">Minh, Inc.</p></li>
  <li><p>#85, 5th Main, P&T<br>
   SanjayNagar, Bangalore<br>
   Karnataka, India 560094<br><br>
   <b>tominhinc@gmail.com</b><br>
   <b>+91 9483160610</b> <img src="<? echo $this->level.'/image/whatsapp_s.png' ?>" width="20px" height="20px"></p>
  </li>
 </ul>
 <ul class="menu">
  <li class="top"><a href="<? echo $this->level ?>/product/">Product</a>
   <ul>
    <li><hr class="product" style="<?php echo ($this->headername=='product'?'background-color:#f38502':'') ?>"></li>
    <li><a href="<? echo $this->level ?>/product/ytd" <? echo ($this->subitem=='ytd'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Youtube Downloader</a><li>
    <li><a href="<? echo $this->level ?>/product/mp" <? echo ($this->subitem=='mp'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Media Player</a><li>
    <li><a href="<? echo $this->level ?>/product/fs" <? echo ($this->subitem=='fs'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Flight Simulator</a><li>
    <li><a href="<? echo $this->level ?>/product/mas" <? echo ($this->subitem=='mas'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Medical Annotation Software</a><li>
    <li><a href="<? echo $this->level ?>/product/3dv" <? echo ($this->subitem=='3dv'?'style="font-weight:bold;color:#aa4400;"':'') ?>>3D Data Viewer</a><li>
   </ul>
  </li>
  <li class="top"><a href="<? echo $this->level ?>/training/">Training</a>
   <ul>
    <li><hr class="training" style="<?php echo ($this->headername=='training'?'background-color:#f38502':'') ?>"></li>
    <li><a href="<? echo $this->level ?>/training/py" <? echo ($this->subitem=='py'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Python</a></li>
    <li><a href="<? echo $this->level ?>/training/c"  <? echo ($this->subitem=='c'?'style="font-weight:bold;color:#aa4400;"':'') ?>>C</a></li>
    <li><a href="<? echo $this->level ?>/training/qt" <? echo ($this->subitem=='qt'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Qt</a></li>
    <li><a href="<? echo $this->level ?>/training/qml" <? echo ($this->subitem=='qml'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Qml</a></li>
    <li><a href="<? echo $this->level ?>/training/cpp" <? echo ($this->subitem=='cpp'?'style="font-weight:bold;color:#aa4400;"':'') ?>>C++</a></li>
    <li><a href="<? echo $this->level ?>/training/gl" <? echo ($this->subitem=='gl'?'style="font-weight:bold;color:#aa4400;"':'') ?>>OpenGL</a></li>
    <li><a href="<? echo $this->level ?>/training/ldd" <? echo ($this->subitem=='ldd'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Linux Device Driver</a></li>
    <li><a href="<? echo $this->level ?>/training/li" <? echo ($this->subitem=='li'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Linux Internals</a></li>
    <li><a href="<? echo $this->level ?>/training/dp" <? echo ($this->subitem=='dp'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Design Patterns</a></li>
   </ul>
  </li>
  <li class="top"><a href="<? echo $this->level ?>/research/">Research</a>
   <ul>
    <li><hr class="research" style="<?php echo ($this->headername=='research'?'background-color:#f38502':'') ?>"></li>
   </ul>
  </li>
  <li class="top"><a href="<? echo $this->level ?>/service/">Services</a>
   <ul>
    <li><hr class="services" style="<?php echo ($this->headername=='service'?'background-color:#f38502':'') ?>"></li>
    <li><a href="<? echo $this->level ?>/service/network" <? echo ($this->subitem=='network'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Networking</a><li>
    <li><a href="<? echo $this->level ?>/service/multimedia" <? echo ($this->subitem=='multimedia'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Multimedia</a></li>
    <li><a href="<? echo $this->level ?>/service/medicalsystem" <? echo ($this->subitem=='medicalsystem'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Medical Systems</a></li>
   </ul>
  </li>
  <li class="top"><a href="<? echo $this->level ?>/career/">Career</a>
   <ul>
    <li><hr class="career" style="<?php echo ($this->headername=='career'?'background-color:#f38502':'') ?>"></li>
   </ul>
  </li>
  <li class="top"><a href="<? echo $this->level ?>/about/">Help</a>
   <ul>
    <li><hr class="help" style="<?php echo ($this->headername=='about'?'background-color:#f38502':'') ?>"></li>
    <li><a href="<? echo $this->level ?>/online" <? echo ($this->subitem=='online'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Online Training</a></li>
    <li><a href="<? echo $this->level ?>/about/question" <? echo ($this->subitem=='question'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Ask a programming question</a></li>
    <li><a href="<? echo $this->level ?>/about/contact" <? echo ($this->subitem=='contact'?'style="font-weight:bold;color:#aa4400;"':'') ?>>Contact Us</a></li>
   </ul>
  </li>
 </ul>
 <ul class="fr">
  <li><p>&copy Minh Inc 2015-<? echo date("Y"); ?></p></li>
<?
echo '<li class="img">';
foreach(Array(Array('https://github.com/minhinc',$this->level.'/image/githubs.png',$this->level.'/image/githubscolor.png'),Array('https://linkedin.com/in/pravinkumarsinha',$this->level.'/image/linkedins.png',$this->level.'/image/linkedinscolor.png'),Array('https://facebook.com/minhinc',$this->level.'/image/fbs.png',$this->level.'/image/fbscolor.png'),Array('http://www.youtube.com/channel/UChmiKM2jr7e9iUOrVPKRTXQ',$this->level.'/image/youtube.png',$this->level.'/image/youtubecolor.png')) as $element){
echo '<a href="'.$element[0].'"><img width="25" height="25" onmouseover=\'this.src="'.$element[2].'"\' onmouseout=\'this.src="'.$element[1].'"\' src="'.$element[1].'"/></a>';
}
echo '</li>';
?>
 </ul>
</div>
</body>
</html>
<?
}

public function drawmenuleft(){
$light="light";
$json=json_decode(mysqli_fetch_row($this->db->get('headername','content','name',$this->headername))[0],true);
echo '<div class="downloadleft">
<ul class="tablist">
<a href="'.$this->level.'/'.$this->headername.'"><li class="header"><p>'.json_decode(mysqli_fetch_row($this->db->get('headername','content','name',$this->headername))[0],true)['title'].'</p></li></a>';
foreach($json['child'] as $key){
if($this->subitem == $key){
echo '<li class="current"><p class="padtop">'.json_decode(mysqli_fetch_row($this->db->get('headername','content','name',$key))[0],true)['title'].'</p></li>';
}else{
echo '<a href="'.$level.'/'.$this->headername.'/'.$key.'"><li class='.$light.'><p>'.json_decode(mysqli_fetch_row($this->db->get('headername','content','name',$key))[0],true)['title'].'</p></li></a>';
}
if($light=="light"){$light="dark";}else{$light="light";}
}
echo ' </ul>
<py>requestm.adsensepaste(0,0,backend="")</py>
</div>';
}

}
?>
