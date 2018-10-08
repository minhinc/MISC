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
<form class="common" action="'.$level.'/php/send_form_email.php" method="post" target="myIframe"">
<h1>Reach Out To Us</h1>
<p>Name:<input type="text" name="name" placeholder="Your Name"></p>
<p>Email:<input type="text" name="email" placeholder="Email Address"></p>
<p class="txtar">Message:<textarea rows="5" name="message" cols="40"></textarea></p>
<input type="submit" name="submit" value="Submit">
<!--<iframe name="myIframe" frameborder="0" height="35px" width="200px" scrolling="no">-->
<iframe name="myIframe" frameborder="0" scrolling="no">
</iframe>
</form>';
}
?>
