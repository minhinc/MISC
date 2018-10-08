<?php
function draw($util){
$util->drawmenuleft();
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$util->headername))[0],true);
echo '<div class="serviceright">
<ul class="desservice">
<li class="header"><p>'.$json['subtitle'].'</p></li>
<li class="dark"><p>'.$json['description'].'</p></li>';
$left=TRUE;
foreach($json['child'] as $key){
$item=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$key))[0],true);
if($left){
echo '<li class="light"><div class="l"><img src="'.$util->level.'/image/'.$key.'.png"/><div><p>'.$item['title'].' - '.$item['description'].'</p><a class="red italic" href="'.$util->level.'/service/'.$key.'">...read more</a></div></div>';
}else{
echo '<div class="r"><img src="'.$util->level.'/image/'.$key.'.png"/><div><p>'.$item['title'].' - '.$item['description'].'</p><a class="red italic" href="'.$util->level.'/service/'.$key.'">...read more</a></div></div></li>';
}
$left=!$left;
}
if(!$left){
echo '</li>';
}
echo '</ul>
</div>';
}
?>
