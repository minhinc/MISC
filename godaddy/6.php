<?php
function draw($util){
$util->drawmenuleft();
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$util->subitem))[0],true);
echo '<div class="serviceright">
<ul class="desservice">
<li class="header"><p>'.ucfirst($util->subitem).'</p></li>
<li class="dark"><p>Company has following products in '.$json['title'].'</p></li>';
$first=TRUE;
$light="";
foreach(json_decode(mysqli_fetch_row($util->db->get('headername','content','name','product'))[0],true)['child'] as $key){
$item=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$key))[0],true);
if(in_array($util->subitem,$item['service'])){
if($first){
if($light=="light"){$light="dark";}else{$light="light";}
echo '<li class="'.$light.'"><div class="l"><img src="'.$util->level.'/image/'.$key.'.png"/><div><p>'.$item['title'].' - '.$item['description'].'</p><a class="btnBlueGloss" href="'.$util->level.'/product/'.$key.'">... more</a></div></div>';
}else{
echo '<div class="r"><img src="'.$util->level.'/image/'.$key.'.png"/><div><p>'.$item['title'].' - '.$item['description'].'</p><a class="btnBlueGloss" href="'.$util->level.'/product/'.$key.'">... more</a></div></div></li>';
}
$first=!$first;
}
}
if(!empty($light) and !$first){
echo '</li>';
}
echo '</ul>
</div>';
}
?>
