<?php
function draw($util){
echo '<div class="leftpan">
 <a href="./about/online"><img src="./image/traininglogo.png"/></a>
 <div class="research">
  <ul class="research">
   <a href="./research/home.html"><li class="header"><p>Research</p></li></a>';
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
   <a href="./product/home.html"><li class="header"><p>Product</p></li></a>';
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name','product'))[0],true);
$light="light";
foreach($json['child'] as $key){
$item=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$key))[0],true);
echo '   <a href="'.$item['link'].'"><li class="'.$light.'"><p class="t">'.$item['title'].'</p><p class="bp">'.$item['date'].'</p><img src="'.$level.'/image/'.$key.'.png"/></li></a>';
if($light=='light'){$light='dark';}else{$light='light';}
}
echo '  </ul>
  </div>
</div>
<div class="rightpan">
 <ul class="events">
  <li class="header"><p>Upcoming Events</p></li>';
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name','main'))[0],true);
$light="light";
foreach($json['event'] as $key){
echo  '<li class="'.$light.'"><p class="t">'.$key['title'].'</p><p class="b">'.$key['date'].'</p></li>';
if($light=='light'){$light='dark';}else{$light='light';}
}
echo ' </ul>
 <ul class="next">
  <a href="./training.home.html"><li class="header"><p>Training</p></li></a>';
$first=TRUE;$light="light";$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name','training'))[0],true);
foreach($json['child'] as $key){
$item=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$key))[0],true);
if($first){
echo '<li class="'.$light.'"><a class="ls" href="./training/'.$key.'/advance-'.$key.'-slides.php">Slides</a><a href="./training/'.$key.'"><img class="l" src="./image/'.$key.'.png"/></a>';
$first=!$first;
}else{
echo '<a class="rs" href="./training/'.$key.'/advance-'.$key.'-slides.php">Slides</a><a href="./training/'.$key.'"><img class="r" src="./image/'.$key.'.png"/></a></li>';
$first=!$first;
if($light=="light"){$light="dark";}else{$light="light";}
}
}
if(!$first){
echo '</li>';
}
echo ' </ul>
</div>'; 
}
?>
