<?php
function draw($util){
$util->drawmenuleft();
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$util->subitem))[0],true);
$first=TRUE;
echo '<div class="downloadright">
<ul class="screenshot">
<li class="header"><p>Screenshots</p></li>';
foreach($json['image'] as $key){
if($first){
echo '<li> <img src="'.$util->level.'/image/'.$key.'"/>';
}else{
echo '<img src="'.$util->level.'/image/'.$key.'"/></li>';
}
$first=!$first;
}
if(!$first){
echo '</li>';
}
echo '</ul>
<ul class="download">
<li class="header"><p>Download</p></li>
<li class="top"><p class="begin"/><p class="long">32bit</p></li>
<li class="top"><p class="begin"/><p class="short">installer(MB)</p><p class="short">zip(MB)</p></li>';
if(!empty($json['download'])){
echo '<li class="light"><p class="begin">Windows 7</p><a class="short" href="'.$util->level.'/binary/'.$json['download']['win32'][0].'">'.$json['download']['win32'][0].'</a><a class="short" href="'.$util->level.'/binary/'.$json['download']['win32'][1].'">'.$json['download']['win32'][1].'</a></li>';
}
echo ' </ul>
</div>';
}
?>
