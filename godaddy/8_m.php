<?php
function draw($util){
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$util->headername))[0],true);
echo '<ul class="eight">
<li class="header"><pre class="header">Profile</pre></li>
<li class="light"><pre>Minh, Inc., based in Bangalore(IN), is a leading research and development company in Multimedia, Network and Medical Systems Software.

Minh, Inc. company provides services in software engineering, predominantly in the field of Network, Multmedia and Medical Systems software based on Python and Qt/Qml.<a class="btnBlueGloss" href="'.$util->level.'/service/">Services</a>

Minh, Inc. has strong two years software development expertise in developing quality software application.<a class="btnBlueGloss" href="'.$util->level.'/product/">Product</a></pre></li>
</ul>
<div class="clr"></div>';
}
?>
