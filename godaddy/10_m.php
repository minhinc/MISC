<?php
function form($util,$tech,$state){
if ($state=='form') {
$min=1;
$max=300;
$num1=rand( $min, $max );
$num2=rand( $min, $max );
$sum=$num1 + $num2;
echo '<style>
#map {
height:248px;
width:359px;
}
</style>
<ul class="ten">
<li class="header"><pre class="header">CONTACT US</pre></li>
<li class="main">
<div style="clear:both;float:left;width:49%;" id="map"></div>
<script>
function initMap(){
var uluru={lat:13.035357,lng:77.576285};
var map=new google.maps.Map(document.getElementById("map"),{ zoom:4, center:uluru });
var marker=new google.maps.Marker({ position:uluru, map:map });
}
</script>
<script async defer
src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCypT5QJIhCg6kqW808Rsn-mXl-dJVtw0M&callback=initMap">
</script>
<div class="right"><pre class="name" style="margin-left:10%">Minh, Inc.</pre><pre class="f10" style="margin-left:10%;">#85<br>5th Main<br>P&T Colony<br>SanjayNagar<br>Bangalore-94</pre><pre class="phone f10 bold" style="margin-left:10%">+91 9483160610 <img src="'.$util->level.'/image/whatsapp.png" width="20px" height="20px"></pre><pre class="f10 bold" style="margin-top:8px;margin-left:10%;color:#4080ff;"><a href="mailto:tominhinc@gmail.com">tominhinc@gmail.com</a></pre></div>
</li>
<li class="form">
<a href="http://minhinc.42web.io/training/'.$tech.'"><img style="margin-left:31%;width:38%" src="http://minhinc.42web.io/image/'.$tech.'traininglogo.gif"></img></a>
<form class="online" action="" method="post" enctype="multipart/form-data" style="float:left">
<h1>Reach Out To Us</h1>
<form class="online" action="" method="post" enctype="multipart/form-data">
<div class="row"><pre class="lc bold">Name:</pre><input type="text" name="name" placeholder="Your Name" class="l"></div>
<div class="row"><pre class="lc bold">Email:</pre><input id="emailid" type="text" name="email" placeholder="Email Address" class="l"><pre class="ls bold star">*</pre></div>
<div class="rowtextarea" ><pre class="lc bold">Comment:</pre><textarea id="messageid" rows="5" name="message" cols="40" class="l2" ></textarea><pre class="ls bold star">*</pre></div>
<div class="row" style="margin-top:20px"><pre class="lc bold" id="quiztextid" style="font-size:14pt;color:#ff0000">'.$num1.'+'.$num2.' ?</pre><input type="text" class="quiz-control l"> <pre class="ls bold star">*</pre></div>
<div class="row" style="margin-top:20px"><input data-res="'.$sum.'" type="submit" name="submit" value="Submit" class="submit lc bold disable" id="s_submit"><pre class="l3" id="iframeid" style="margin-left:5%;font-size:14pt;font-weight:bold;height:30"></pre></div>
</form>
</li>
</ul>
<div style="clear:both"></div>
<script>
const emailregex = /^([\w\d._\-#])+@([\w\d._\-#]+[.][\w\d._\-#]+)+$/;
function submitenabledisable() {
 if ( document.getElementById("messageid").value.length<1 || !document.getElementById("emailid").value.match(emailregex) || document.querySelector(".quiz-control").value!=document.getElementById("s_submit").getAttribute("data-res")) {
 document.getElementById("s_submit").classList.remove("enable");
 document.getElementById("s_submit").classList.add("disable");
 document.getElementById("s_submit").disabled=true;
 } else {
 document.getElementById("s_submit").classList.remove("disable");
 document.getElementById("s_submit").classList.add("enable");
 document.getElementById("s_submit").disabled=false;
 }
}
const emailInput = document.getElementById("emailid");
emailInput.addEventListener("input", function(e) {
 if ( this.value.match(emailregex) ) {
  this.style.removeProperty("border");
 } else {
 this.style.border="1px solid red";
 }
submitenabledisable();
});

const messageInput = document.getElementById("messageid");
messageInput.addEventListener("input", function(e) {
 if ( this.value.length>0 ) {
 this.style.removeProperty("border");
 } else {
 this.style.border="1px solid red";
 }
submitenabledisable();
});

const submitButton = document.getElementById("s_submit");
const quizInput = document.querySelector(".quiz-control");
quizInput.addEventListener("input", function(e) {
const res = submitButton.getAttribute("data-res");
if ( this.value == res ) {
this.style.removeProperty("border");
document.getElementById("quiztextid").style.color="blue";
} else {
this.style.border="1px solid red";
document.getElementById("quiztextid").style.color="red";
}
submitenabledisable();
});
submitenabledisable();
</script>';
} else
 echo $state;
}
function draw($util){
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$util->subitem))[0],true);
$tech=json_decode(mysqli_fetch_row($util->db->get('headername','content','name','training'))[0],true)['child'];
$tech=$tech[rand(0,count($tech)-1)];
$email_exp = '/^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$/';
 if(isset($_POST['submit'])){
  $filedata=file_get_contents('../../online/message.txt');
  $filedata=$filedata."\n".$_POST['name']."!ABS SBA!".$_POST['email']."!ABS SBA!".preg_replace("/\r\n/","\\n",$_POST['message'])."!ABS SBA!".date('d-m-y h:i:s');
  $message="Name- ".$_POST['name']."\n"."Email- ".$_POST['email']."\n"."Message- ".$_POST['message'];
  file_put_contents('../../online/message.txt',$filedata);
  form($util,$tech,"<pre style=\"color:#444444;font-size:18pt;text-align:center\">".$message."</pre><br><br><pre style=\"color:#004000;font-size:28pt;text-align:center\">Message Sent.</pre>");
 }else
  form($util,$tech,'form');
}
?>
