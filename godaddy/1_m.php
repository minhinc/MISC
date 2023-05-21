<?php
function draw($util){
echo '<a href="https://www.youtube.com/c/minhinc"><img class="traininglogo" src="./image/main_front.png"/></img></a>
 <div class="one"> <ul class="events">
  <li class="header"><p>Upcoming Events</p></li>';
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name','main'))[0],true);
$light="light";
foreach($json['event'] as $key){
echo  '<a href="'.$key['link'].'"><li class="'.$light.'"><p class="t">'.$key['title'].'</p><p class="b">'.((date("d") < 15)?date("M Y"):date("M Y",strtotime("+1 month"))).'</p></li></a>';
if($light=='light'){$light='dark';}else{$light='light';}
}
echo '</ul></div>';
$light="light"; $first=TRUE; $link="";
foreach (array('training','research','product') as $research){
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$research))[0],true);
echo '  <li class="adsense100"><!--<py>requestm.adsensepaste(0,100,backend="mobile")</py>--></li>';
echo '<div class="one"><a href="'.$json['link'].'"><pre class="title">'.ucfirst($research).'</pre></a><pre class="subtitle">'.$json['description'].'</pre></div>';
echo ' <ul class="one">';
$light="light";
foreach($json['child'] as $key){
$item=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$key))[0],true);
if(empty($item['link'])){
$link=$util->level.'/'.$research.'/'.$key;
}else{
$link=$item['link'];
}
echo '  <li class="'.$light.'"><a href="'.$link.'"><img src="'.$util->level.'/image/'.$key.'.png"/><pre>'.$item['title'].'</pre></a></li>';
if ($light=="light"){
$light="dark";
}else{
$light="light";
}
}
echo ' </ul>
<div style="clear:both"></div>';
}
}
?>
