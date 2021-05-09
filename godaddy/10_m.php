<?php
function draw($util){
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
<div class="r"><pre class="name" style="margin-left:10%">Minh, Inc.</pre><pre class="f10" style="margin-left:10%;">#85<br>5th Main<br>P&T Colony<br>SanjayNagar<br>Bangalore-94</pre><pre class="phone f10 bold" style="margin-left:10%">+91 9483160610 <img src="'.$util->level.'/image/whatsapp.png" width="20px" height="20px"></pre><pre class="f10 bold" style="margin-top:8px;margin-left:10%;color:#4080ff;"><a href="mailto:sales@minhinc.com">sales@minhinc.com</a></pre></div>
</li>
<div class="clr"></div><li class="adsense100"><py>requestm.adsensepaste(0,100,backend="mobile")</py></li>
<li class="form">
<form class="online" action="'.$util->level.'/php/send_form_email.php" method="post" target="myIframe">
<h1>Reach Out To Us</h1>
<div class="row"><pre class="lc bold">Name:</pre><input type="text" name="name" placeholder="Your Name" class="l"></div>
<div class="row"><pre class="lc bold">Email:</pre><input id="emailid" type="text" name="email" placeholder="Email Address" class="l"></div>
<div class="rowtextarea"><pre class="lc bold">Query:</pre><textarea id="textareaid" rows="5" name="message" cols="40" class="l2"></textarea></div>
<div style="margin:10px 0" class="g-recaptcha" data-callback="imNotARobot" data-sitekey="6LdifdsZAAAAAMU2aqKdvbKtFjph29dqaHAp4Xqj"></div>
<div class="row"><input type="submit" name="submit" value="Submit" class="submit lc bold enable"><iframe name="myIframe" frameborder="0" scrolling="no" class="l" id="iframeid"></iframe></div>
</form>
<div style="clear:both"></div>
</li>
</ul>
<div class="clr"></div>
<script>
var imNotARobot = function() {
 document.getElementById("iframeid").contentWindow.document.write("");
};
document.getElementById("iframeid").onload=function(){
 var framecontent=document.getElementById("iframeid").contentWindow.document.body.innerHTML;
  if (framecontent.match(/40/gi)){
   document.getElementById("emailid").value="";
   document.getElementById("textareaid").value="";
   grecaptcha.reset();
  }
}
</script>';
}
?>
