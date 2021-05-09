<?php
function draw($util){
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$util->subitem))[0],true);
echo '<style>
#map {
height:248px;
width:359px;
}
</style>
<ul class="contact">
<li class="header"><p>CONTACT US</p></li>
<li class="main">
<div id="map"></div>
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
<div class="r"><p class="b" style="font-family:mytwcenmt;font-size:24pt;color:#004000">Minh, Inc.</p><div class="dl"><p class="n">Tel: +91 9483160610<img src="'.$util->level.'/image/whatsapp.png" width="20px" height="20px"> <br>Email: <a href="mailto:sales@minhinc.com"><span class="green">sales@minhinc.com</span></a></p></div><div class="dr"><p>#85<br>5th Main<br>P&T Colony<br>SanjayNagar<br>Bangalore-94</p></div></div>
</li>
</ul>
<py>requestm.adsensepaste(950,250,backend="desktop",factor=0.0)</py>
<form class="online" action="'.$util->level.'/php/send_form_email.php" method="post" target="myIframe">
<h1>Reach Out To Us</h1>
 <div class="row"><pre class="lc bold">Name:</pre><input type="text" name="name" placeholder="Your Name" class="l"></div>
 <div class="row"><pre class="lc bold">Email:</pre><input id="emailid" type="text" name="email" placeholder="Email Address" class="l"></div>
 <div class="rowtextarea"><pre class="lc bold">Query:</pre><textarea id="textareaid" rows="5" name="message" cols="40" class="l2"></textarea></div>
 <div style="margin:10px 0" class="g-recaptcha" data-callback="imNotARobot" data-sitekey="'.preg_replace('/^(.*)\\n.*/m','$1',file_get_contents($util->level.'/donotdelete/captchav2/sitecaptchav2.key')).'"></div>
 <div class="row"><input type="submit" name="submit" value="Submit" class="submit lc bold enable"><iframe name="myIframe" frameborder="0" scrolling="no" class="l" style="width:400px" id="iframeid"></iframe></div>
 </form>
 <div style="clear:both"></div>
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
