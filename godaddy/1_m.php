<?php
function draw($util){
echo '<a href="./about/online"><img class="traininglogo" src="./image/traininglogo.png"/></img></a>';
$light="light"; $first=TRUE; $link="";
foreach (array('training','product','research') as $research){
echo ' <ul class="one">
  <li class="header"><a href="'.$util->level.'/'.$research.'"><pre class="header">'.ucfirst($research).'</pre></a></li>';
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$research))[0],true);
$light="light";
$first=TRUE;
foreach($json['child'] as $key){
$item=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$key))[0],true);
if(empty($item['link'])){
$link=$util->level.'/'.$research.'/'.$key;
}else{
$link=$item['link'];
}
if($first){
echo '  <li class="'.$light.'"><div class="l"><div class="l"><a href="'.$link.'"><pre>'.$item['title'].'</pre></a></div><div class="r"><img src="'.$util->level.'/image/'.$key.'.png"/></div></div>';
}else{
echo '<div class="r"><div class="l"><a href="'.$link.'"><pre>'.$item['title'].'</pre></a></div><div class="r"><img src="'.$util->level.'/image/'.$key.'.png"/></div></div></li>';
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
}
?>
