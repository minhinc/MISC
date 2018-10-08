<?php
function draw($util){
$util->drawmenuleft();
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$util->headername))[0],true);
echo '<div class="downloadright">
<ul class="description">
<li class="header"><p>Profile</p></li>
<li class="light"><p>Minh, Inc., based in Bangalore(IN), is a leading research and development company in Multimedia, Network and Medical Systems Software.<br><br>Minh, Inc. company provides services in software engineering, predominantly in the field of Network, Multmedia and Medical Systems software based on Python and Qt/Qml.<a class="btnBlueGloss" href="'.$level.'/service/">Services</a><br><br>Minh, Inc. has strong two years software development expertise in developing quality software application.<a class="btnBlueGloss" href="'.$level.'/product/">Product</a></p></li>
</ul>
</div>';
}
?>
