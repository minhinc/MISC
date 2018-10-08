<?php
function draw($util){
$light="light";$first=TRUE;$link='';
echo ' <ul class="two"">
<li class="header"><pre class="header">'.ucfirst($util->headername).'</pre></li>
<li><div class="l"><img src="'.$level.'/image/'.$util->headername.'.png"/></div><div class="r"><pre class="bold">'.$util->json['subtitle'].'</pre><pre>'.$util->json['description'].'</pre></div></li>';
$light="light";
$first=TRUE;
foreach($util->json['child'] as $key){
$item=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$key))[0],true);
if(empty($item['link']))
 $link=$util->level.'/'.$util->headername.'/'.$key;
else
 $link=$item['link'];
if($first){
echo '  <li><div class="l"><div class="ll"><img src="'.$util->level.'/image/'.$key.'.png"/></div><div class="rr"><a href="'.$link.'"><pre class="bold gold">'.$item['title'].'</pre><pre>'.$item['description'].'</pre></a><a class="space"></a><pre class="space">'.$item['date'].'</pre></div></div>';
}else{
echo '<div class="r"><div class="ll"><img src="'.$util->level.'/image/'.$key.'.png"/></div><div class="rr"><a href="'.$link.'"><pre class="bold gold">'.$item['title'].'</pre><pre>'.$item['description'].'</pre></a><a class="space"></a><pre class="space">'.$item['date'].'</pre></div></div></li>';
if($light=='light'){$light='dark';}else{$light='light';}
}
$first=!$first;
}
if(!$first){
echo '  </li>';
}
echo ' </ul>
<div style="clear:both"></div>';
}
?>
