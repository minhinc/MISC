<?php
function draw($util){
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$util->subitem))[0],true);
echo '<ul class="five">
<li class="header"><pre>'.ucfirst($util->subitem).'</pre></li>
<li class="dark" style="margin-bottom:10px"><pre>Company has following products in '.$json['title'].'</pre></li>';
$first=TRUE;
$light="";
foreach(json_decode(mysqli_fetch_row($util->db->get('headername','content','name','product'))[0],true)['child'] as $key){
$item=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$key))[0],true);
if(in_array($util->subitem,$item['service'])){
if($first){
if($light=="light"){$light="dark";}else{$light="light";}
echo '<li class="'.$light.'"><div class="l"><img class="ll" src="'.$util->level.'/image/'.$key.'.png"/><div class="rr"><pre>'.$item['title'].' - '.$item['description'].'</pre><a class="btnBlueGloss" href="'.$util->level.'/product/'.$key.'">... more</a></div></div>';
}else{
echo '<div class="right"><img class="ll" src="'.$util->level.'/image/'.$key.'.png"/><div class="rr"><pre>'.$item['title'].' - '.$item['description'].'</pre><a class="btnBlueGloss" href="'.$util->level.'/product/'.$key.'">... more</a></div></div></li>';
}
$first=!$first;
}
}
if(!empty($light) and !$first){
echo '</li>';
}
echo '</ul>
<div style="clear:both"></div>';
}
?>
