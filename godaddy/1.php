<?php
function draw($util){
echo '<div class="leftpan">
 <a href="https://www.youtube.com/c/minhinc"><img src="./image/main_front.png"/></a>
<!-- <py>requestm.adsensepaste(640,60,backend="desktop",factor=0.0)</py> -->
 <div class="research">
  <ul class="research">
   <a href="./research/"><li class="header"><p>Research</p></li></a>';
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name','research'))[0],true);
$light="light";
foreach($json['child'] as $key){
$item=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$key))[0],true);
echo'   <a href="'.$item['link'].'"><li class="'.$light.'"><p class="t">'.$item['title'].'</p><p class="b">'.$item['publisher'].','.$item['date'].'</p><img src="'.$level.'/image/'.$key.'.png"/></li></a>';
if($light=='light'){$light='dark';}else{$light='light';}
}
echo '  </ul>
  </div>
  <div class="product">
  <ul class="research">
   <a href="./product/"><li class="header"><p>Product</p></li></a>';
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name','product'))[0],true);
$light="light";
foreach($json['child'] as $key){
$item=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$key))[0],true);
echo '   <a href="'.$item['link'].'"><li class="'.$light.'"><p class="t">'.$item['title'].'</p><p class="bp">'.$item['date'].'</p><img src="'.$level.'/image/'.$key.'.png"/></li></a>';
if($light=='light'){$light='dark';}else{$light='light';}
}
echo '  </ul>
 <!-- <py>requestm.adsensepaste(310,450,backend="desktop",factor=0.0)</py> -->
  </div>
</div>
<div class="rightpan">
 <ul class="events">
  <li class="header"><p>Upcoming Events</p></li>';
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name','main'))[0],true);
$light="light";
foreach($json['event'] as $key){
echo  '<a href="'.$key['link'].'"><li class="'.$light.'"><p class="t">'.$key['title'].'</p><p class="b">'.((date("d") < 15)?date("M Y"):date("M Y",strtotime("+1 month"))).'</p></li></a>';
if($light=='light'){$light='dark';}else{$light='light';}
}
echo ' </ul>
<!-- <py>requestm.adsensepaste(310,60,backend="desktop")</py> -->
 <ul class="next">
  <a href="./training/"><li class="header"><p>Training</p></li></a>';
$first=TRUE;$light="light";$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name','training'))[0],true);
foreach($json['child'] as $key){
$item=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$key))[0],true);
if($first){
echo '<li class="'.$light.'"><a class="ls" href="./training/'.$key.'">Slides</a><a href="./training/'.$key.'"><img class="l" src="./image/'.$key.'.png"/></a>';
$first=!$first;
}else{
echo '<a class="rs" href="./training/'.$key.'">Slides</a><a href="./training/'.$key.'"><img class="r" src="./image/'.$key.'.png"/></a></li>';
$first=!$first;
if($light=="light"){$light="dark";}else{$light="light";}
}
}
if(!$first){
echo '</li>';
}
echo ' </ul>
<!-- <py>requestm.adsensepaste(310,500,backend="desktop",factor=0.0)</py> -->
</div>'; 
}
?>
