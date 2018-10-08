<?php
function draw2_1($util){
$light="light";
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$util->headername))[0],true);
echo '<ul class="common">
 <li class="header"><p>'.strtoupper($util->headername).'</p></li>
 <li class="main"><img src="'.$util->level.'/image/'.$json['id'].'.png"/><div><p class="b">'.ucfirst($json['subtitle']).'</p><p class="n">'.$json['description'].'</p></div></li>';
$count=1;
foreach ($json['child'] as $key){
$child=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$key))[0],true);
if($count % 2){
echo '<li class="entry"><a href="'.$child['link'].'"><div class="dl"><img src="'.$util->level.'/image/'.$child['id'].'.png"/><div><p class="b">'.$child['title'].'</p><p>'.$child['description'].'</p><a class="space"></a><p class="space">'.$child['date'].'</p></div></div></a>';
}else{
echo '<a href="'.$child['link'].'"><div class="dr"><img src="'.$util->level.'/image/'.$child['id'].'.png"/><div><p class="b">'.$child['title'].'</p><p>'.$child['description'].'</p><a class="space"></a><p class="space">'.$child['date'].'</p></div></div></a></li>';
}
++$count;
}
echo ' </ul>';
}
?>
