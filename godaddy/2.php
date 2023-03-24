<?php
function draw($util){
$light="light";
$code="";
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$util->headername))[0],true);
echo '<ul class="common">
 <li class="header"><p>'.strtoupper($util->headername).'</p></li>
 <li class="main"><img src="'.$util->level.'/image/'.$util->headername.'.png"/><div><p class="b">'.ucfirst($json['subtitle']).'</p><p class="n">'.$json['description'].'</p></div></li>';
$count=1;
foreach ($json['child'] as $key){
$item=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$key))[0],true);
if (!empty($item['code'])){$code='<a style="float:left;margin-left:5px;margin-top:4px;height:10px;border:1px solid #f38502;padding:2px;font-size:6pt;font-weight:bold;" href="'.$item['code'].'">code</a>';}else{$code='';}
if($count % 2){
echo '<li style="height:90px;clear:both;"><div style="width:960px;height:90px;position:relative;" align="center"><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- fixed_728_90 -->
<ins class="adsbygoogle"
     style="position:absolute;left:116px;top:0px;display:inline-block;width:728px;height:90px"
     data-ad-client="ca-pub-8488699542117607"
     data-ad-slot="2670898784"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script></div></li>';
echo '<li class="entry"><a href="'.$item['link'].'"><div class="dl"><img src="'.$util->level.'/image/'.$key.'.png"/><div><p class="b">'.$item['title'].'</p><p>'.$item['description'].'</p><a class="space"></a><p class="space">'.$item['date'].'</p>'.$code.'</div></div></a>';
}else{
echo '<a href="'.$item['link'].'"><div class="dr"><img src="'.$util->level.'/image/'.$key.'.png"/><div><p class="b">'.$item['title'].'</p><p>'.$item['description'].'</p><a class="space"></a><p class="space">'.$item['date'].'</p>'.$code.'</div></div></a></li>';
}
++$count;
}
if($count %2 == 0)
 echo '</li>';
echo ' </ul>';
}
?>
