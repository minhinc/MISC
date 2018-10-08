<?php
function draw($util){
$light="light";
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$util->headername))[0],true);
echo '<ul class="common">
 <li class="header"><p>'.strtoupper($util->headername).'</p></li>
 <li class="main"><img src="'.$util->level.'/image/'.$util->headername.'.png"/><div><p class="b">'.ucfirst($json['subtitle']).'</p><p class="n">'.$json['description'].'</p></div></li>';
$count=1;
foreach ($json['child'] as $key){
$item=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$key))[0],true);
if($count % 2){
echo '<li class="entry"><a href="'.$item['link'].'"><div class="dl"><img src="'.$util->level.'/image/'.$key.'.png"/><div><p class="b">'.$item['title'].'</p><p>'.$item['description'].'</p><a class="space"></a><p class="space">'.$item['date'].'</p></div></div></a>';
}else{
echo '<a href="'.$item['link'].'"><div class="dr"><img src="'.$util->level.'/image/'.$key.'.png"/><div><p class="b">'.$item['title'].'</p><p>'.$item['description'].'</p><a class="space"></a><p class="space">'.$item['date'].'</p></div></div></a></li>';
}
++$count;
}
echo ' </ul>';
}
?>
