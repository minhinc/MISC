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
$json=json_decode(mysqli_fetch_row($this->db->get('headername','content','name','main'))[0],true);
$fontsize="10";$link="";$fontmargin=30;
echo '<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" type="text/css" href="'.$this->level.'/css/main_m.css" media="all"/>
<link rel="stylesheet" type="text/css" href="'.$this->level.'/css/agenda_m.css" media="all"/>
</head>
<body>';
include_once('analyticstracking.php');
echo '<div class="menubar">
 <a href="'.$this->level.'"><img class="homelogo" src="'.$this->level.'/image/topconLogo.png"/></a>
  <img onclick="myFunction()" class="linelogo" src="'.$this->level.'/image/menulogo.png"></img>
  <div id="myDropdown" class="dropdown-content">';
foreach($json['child'] as $key){
echo '<div class="line"><div class="l"><a href='.$this->level.'/'.$key.'>'.ucfirst($key).'</a></div><div class="r linesubmenu" onclick="myFunction1(\'linesubmenu\')"><div class="tr"></div></div></div>
<div class="submenu">';
$json1=json_decode(mysqli_fetch_row($this->db->get('headername','content','name',$key))[0],true);
foreach($json1['child'] as $key1){
$fontsize="10";
if(empty(json_decode(mysqli_fetch_row($this->db->get('headername','content','name',$key1))[0],true)['link']))
 $link=$this->level.'/'.$key.'/'.$key1;
else
 $link=json_decode(mysqli_fetch_row($this->db->get('headername','content','name',$key1))[0],true)['link'];
if(strlen(json_decode(mysqli_fetch_row($this->db->get('headername','content','name',$key1))[0],true)['title'])>$fontmargin)
 $fontsize=($fontsize*$fontmargin)/strlen(json_decode(mysqli_fetch_row($this->db->get('headername','content','name',$key1))[0],true)['title']);
echo '<div class="linew"><a href="'.$link.'" style="font-size:'.$fontsize.'pt">'.ucfirst(json_decode(mysqli_fetch_row($this->db->get('headername','content','name',$key1))[0],true)['title']).'</a></div>';
}
echo '</div>';
}
echo ' </div>
</div>';
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
+91 9483160610&nbsp&nbsp<img src="'.$this->level.'/image/whatsapp.png" width="15px" height="15px"/>
</pre>
</div>
<div class="r">';
foreach($json['child'] as $key){
 echo '<div class="fline" style="margin-bottom:10px;"><div class="inline tv footermenu" onclick="myFunction1(\'footermenu\')"></div><a class="inline" style="margin-left:10px;font-size:13px" href="'.$this->level.'/'.$key.'">'.ucfirst($key).'</a></div>
<div class="fsubmenu">';
 $json1=json_decode(mysqli_fetch_row($this->db->get('headername','content','name',$key))[0],true);
 foreach($json1['child'] as $key1){
  if(empty(json_decode(mysqli_fetch_row($this->db->get('headername','content','name',$key1))[0],true)['link']))
   $link=$this->level.'/'.$key.'/'.$key1;
  else
   $link=json_decode(mysqli_fetch_row($this->db->get('headername','content','name',$key1))[0],true)['link'];
  echo '<div class="flinew" style="margin-bottom:5px;"><div class="fltleft ths"></div><a style="margin-left:5px;" href="'.$link.'">'.ucfirst(json_decode(mysqli_fetch_row($this->db->get('headername','content','name',$key1))[0],true)['title']).'</a></div>';
 }
echo '</div>';
}
echo '</div>
<div style="clear:both"></div>
<pre style="text-align:center;margin-top:20px">&copy Minh, Inc 2015-2018</pre>
</div>

<script>
function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
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
  document.getElementById("myDropdown").classList.remove("show");
 }
}
</script>
</body>
</html>';
}
}
?>
