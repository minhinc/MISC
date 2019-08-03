<?
require_once('Utilbm.php');
class Utilc_m extends Utilbc{
public function drawscript(){
echo file_get_contents($this->script.'_m.txt');
}
public function draw(){
require_once($this->json['pattern'].'_m.php');
draw($this);
}
public function drawheader(){
//<script src="../css/main_m.js"></script>
$json['title']='';
if (!empty($this->subitem)) $json=json_decode(mysqli_fetch_row($this->db->get('headername','content','name',$this->subitem))[0],true);
elseif(!empty($this->headername)) $json=json_decode(mysqli_fetch_row($this->db->get('headername','content','name',$this->headername))[0],true);
echo '<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">';
if (empty($this->headername)){
echo '<title>Minh, Inc. Software development and Outsourcing Bangalore India</title>';
}else{
echo '<title>'.$json['title'].' | Minh, Inc. Bangalore India</title>';
}
echo '<link rel="stylesheet" type="text/css" href="'.$this->level.'/css/main_m.css" media="all"/>
<link rel="stylesheet" type="text/css" href="'.$this->level.'/css/agenda_m.css" media="all"/>
</head>
<body>';
include_once('analyticstracking.php');
//$json=json_decode(mysqli_fetch_row($this->db->get('headername','content','name','main'))[0],true);
echo '<div class="menubar">
 <a href="'.$this->level.'"><img class="homelogo" src="'.$this->level.'/image/topconLogo.png"/></a>
  <span class="linelogo" onclick="myFunction()">&#9776;</span>
  <div id="myDropdown" class="dropdown-content">';
echo $this->drawmenu();
echo ' </div>
</div>';

$json=json_decode(mysqli_fetch_row($this->db->get('headername','content','name','main'))[0],true);
if (!empty($json['comingevents']) && $this->headername != "about" && $this->subitem != "online"){
echo '<div style="width:90%;height:40px;margin:10px auto;background-color:#0707a2"><pre style="float:left;padding-left:5%;line-height:40px;color:#ffffff;font-family:mytwcenmt;font-size:10px;">';
echo $json['comingtraining'];
echo '</pre><a href="http://www.minhinc.com/about/online" style="float:right;margin:5px 5%;padding:0px 5px;border-radius:5px;display:block;background-color:#53616e;line-height:30px;font-size:10px;color:#ffffff";font-family:arial, helvetica, sans;>...Know More</a></div><div style="clear:both"></div>';
}
}

public function drawmenu($returnstring=''){
$fontsize="10";$link="";$fontmargin=30;
$json=json_decode(mysqli_fetch_row($this->db->get('headername','content','name','main'))[0],true);
foreach($json['child'] as $key){
 $color='';
 if($key==$this->headername) {$color='style="color:#f38502;font-weight:bold;"';}else{$color='';}
 $returnstring .= '<div class="line"><div class="l"><a '.$color.' href='.$this->level.'/'.$key.'>'.ucfirst($key).'</a></div><div class="r linesubmenu" onclick="myFunction1(\'linesubmenu\')"><div class="tr"></div></div></div>
  <div class="submenu">';
  $json1=json_decode(mysqli_fetch_row($this->db->get('headername','content','name',$key))[0],true);
  foreach($json1['child'] as $key1){
   $fontsize="10";
   if($key1==$this->subitem) {$color=';color:#f38502;font-weight:bold;';}else{$color='';}
   if(empty(json_decode(mysqli_fetch_row($this->db->get('headername','content','name',$key1))[0],true)['link']))
    $link=$this->level.'/'.$key.'/'.$key1;
   else
    $link=json_decode(mysqli_fetch_row($this->db->get('headername','content','name',$key1))[0],true)['link'];
   if(strlen(json_decode(mysqli_fetch_row($this->db->get('headername','content','name',$key1))[0],true)['title'])>$fontmargin)
    $fontsize=($fontsize*$fontmargin)/strlen(json_decode(mysqli_fetch_row($this->db->get('headername','content','name',$key1))[0],true)['title']);
    $returnstring .= '<div class="linew"><a href="'.$link.'" style="font-size:'.$fontsize.'pt;'.$color.'">'.ucfirst(json_decode(mysqli_fetch_row($this->db->get('headername','content','name',$key1))[0],true)['title']).'</a></div>';
  }
 $returnstring .= '</div>';
}
$returnstring .= '<hr class="one">';
if($this->subitem=='online') {$color='style="color:#f38502;font-weight:bold;"';}else{$color='';}
$returnstring .= '<div class="line" style="border-color:transparent"><div class="l"><a '.$color.' href="'.$this->level.'/about/online">Online Training</a></div></div>';
if($this->headername=='training' && $this->subitem=='qt') {$color='style="color:#f38502;font-weight:bold;"';}else{$color='';}
$returnstring .= '<div class="line"><div class="l"><a '.$color.' href="'.$this->level.'/training/qt">Qt Training</a></div></div>';
return $returnstring;
}


public function drawfooter(){
$json=json_decode(mysqli_fetch_row($this->db->get('headername','content','name','main'))[0],true);
echo '<div class="footer">
<div class="l">
<pre style="margin-left:5%;">
Minh, Inc.
#85, 5th Main, P&T
SanjayNagar, Bangalore
Karnataka, India 560094

sales@minhinc.com
+91 9483160610&nbsp&nbsp<img src="'.$this->level.'/image/whatsapp_s.png" width="15px" height="15px"/>
</pre>
</div>
<div class="r">';
foreach($json['child'] as $key){
$color='';
if($key==$this->headername) {$color='color:#f38502;';}else{$color='';}
 echo '<div class="fline" style="margin-bottom:10px;"><div class="inline tv footermenu" onclick="myFunction1(\'footermenu\')"></div><a class="inline" style="margin-left:10px;font-size:13px;'.$color.'" href="'.$this->level.'/'.$key.'">'.ucfirst($key).'</a></div>
<div class="fsubmenu">';
 $json1=json_decode(mysqli_fetch_row($this->db->get('headername','content','name',$key))[0],true);
 foreach($json1['child'] as $key1){
  if($key1==$this->subitem) {$color='color:#f38502;';}else{$color='';}
  if(empty(json_decode(mysqli_fetch_row($this->db->get('headername','content','name',$key1))[0],true)['link']))
   $link=$this->level.'/'.$key.'/'.$key1;
  else
   $link=json_decode(mysqli_fetch_row($this->db->get('headername','content','name',$key1))[0],true)['link'];
  echo '<div class="flinew" style="margin-bottom:5px;"><div class="fltleft ths"></div><a style="margin-left:5px;'.$color.'" href="'.$link.'">'.ucfirst(json_decode(mysqli_fetch_row($this->db->get('headername','content','name',$key1))[0],true)['title']).'</a></div>';
 }
echo '</div>';
}
echo '</div>
<div style="clear:both"></div>
<pre style="text-align:center;margin-top:20px">&copy Minh, Inc 2015-2019</pre>
</div>

<script>
document.getElementById("myDropdown").style.height=document.documentElement.clientHeight-document.getElementById("myDropdown").getBoundingClientRect().top-20+"px";
window.onscroll=function(e){
if(this.oldScroll > this.scrollY){
 document.getElementById("myDropdown").style.height=document.documentElement.clientHeight-document.getElementById("myDropdown").getBoundingClientRect().top-20+"px";
}else{
 document.getElementById("myDropdown").style.height=document.documentElement.clientHeight+"px";
}
this.oldScroll = this.scrollY;
}
function myFunction() {
/*    document.getElementById("myDropdown").classList.toggle("show"); */
 if(document.getElementById("myDropdown").style.width==="70%"){
  document.getElementById("myDropdown").style.width="0";
 }else{
  document.getElementById("myDropdown").style.width="70%";
 }
}

function myFunction1(id){
var i;
var acc=document.getElementsByClassName(id);
 for(i=0;i<acc.length;i++){
  if(acc[i].contains(event.target)){
   var panel=acc[i].parentNode.nextElementSibling;
   if (panel.style.display === "block") {
    acc[i].classList.remove("th");
    acc[i].classList.add("tv");
    panel.style.display = "none";
   } else {
    acc[i].classList.remove("tv");
    acc[i].classList.add("th");
    panel.style.display = "block";
   }
  }
 }
}

/* if (document.getElementsByClassName("linelogo")[0].contains(event.target)){*/
/*window.onclick=function(event) {
 if (!event.target.matches(".myDropdown") && !event.target.matches(".linelogo")) {
    document.getElementById("myDropdown").classList.remove("show");
 }
}*/
window.onclick=function(event) {
 if(!document.getElementById("myDropdown").contains(event.target) && !document.getElementsByClassName("linelogo")[0].contains(event.target)){
  document.getElementById("myDropdown").style.width="0";
  /*document.getElementById("myDropdown").classList.remove("show");*/
 }
}
</script>
</body>
</html>';
}
}
?>
