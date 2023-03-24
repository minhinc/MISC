<?php
function draw($util){
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$util->headername))[0],true);
echo '<ul class="five">
<li class="header"><pre>'.$json['subtitle'].'</pre></li>
<li class="dark" style="margin-bottom:10px"><pre>'.$json['description'].'</pre></li>';
$left=TRUE;
foreach($json['child'] as $key){
$item=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$key))[0],true);
if($left){
echo '<li class="light"><div class="l"><img class="ll" src="'.$util->level.'/image/'.$key.'.png"/><div class="rr"><pre>'.$item['title'].' - '.$item['description'].'</pre><a class="red italic" href="'.$util->level.'/service/'.$key.'">...read more</a></div></div>';
}else{
echo '<div class="right"><img class="ll" src="'.$util->level.'/image/'.$key.'.png"/><div class="rr"><pre>'.$item['title'].' - '.$item['description'].'</pre><a class="red italic" href="'.$util->level.'/service/'.$key.'">...read more</a></div></div></li>';
}
$left=!$left;
}
if(!$left){
echo '</li>';
}
echo '</ul>
<div style="clear:both;"></div>';
}
?>
