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
<li class="form">
<form class="common" action="'.$util->level.'/php/send_form_email.php" method="post" target="myIframe">
<h1>Reach Out To Us</h1>
<div><pre class="bold f10 ll">Name:</pre><input class="rr" style="margin-top:-7px" type="text" name="name" placeholder="Your Name"></input></div>
<div><pre class="bold f10 ll" style="margin-top:30px">Email:</pre><input class="rr" style="margin-top:23px" type="text" name="email" placeholder="Email Address"></input></div>
<div><pre class="bold f10 ll" style="margin-top:30px">Message:</pre><textarea class="rr" style="margin-top:-20px;" name="message"></textarea></div>
<div><img id="imgcaptchaid" src="'.$util->level.'/php/captcha.php" style="margin:10px 0;float:left"/><input name="captcha_entered" type="text" id="captcha_entered" size="5" maxlength="2" placeholder = "Answer" style="margin:10px 10px;float:left"/></div>
<input type="submit" name="submit" value="Submit" style="width:40%;clear:both;float:left">
<iframe name="myIframe" frameborder="0" scrolling="no" id="iframeid">
</iframe>
</form>
</li>
</ul>
<div class="clr"></div>
<script>
document.getElementById("iframeid").onload=function(){
document.getElementById("imgcaptchaid").src="'.$util->level.'/php/captcha.php?time="+new Date();
}
</script>';
}
?>
