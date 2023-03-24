<?php
function draw($util){
$light="light";$first=TRUE;$link='';
$code="";
echo ' <ul class="two">
<li class="header"><pre class="header">'.ucfirst($util->headername).'</pre></li>
<li><div class="l"><img src="'.$level.'/image/'.$util->headername.'.png"/></div><div class="right"><pre class="bold">'.$util->json['subtitle'].'</pre><pre>'.$util->json['description'].'</pre></div></li>';
$light="light";
$first=TRUE;
foreach($util->json['child'] as $key){
$item=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$key))[0],true);
if (!empty($item['code'])){$code='<a style="float:left;margin-left:4px;margin-top:4px;border:1px solid #f38502;padding:2px;font-size:6pt;font-weight:bold;" href="'.$item['code'].'">code</a>';}else{$code='';}
if(empty($item['link']))
 $link=$util->level.'/'.$util->headername.'/'.$key;
else
 $link=$item['link'];
if($first){
echo '  <li><div class="l"><div class="ll"><img src="'.$util->level.'/image/'.$key.'.png"/></div><div class="rr"><a href="'.$link.'"><pre class="bold gold">'.$item['title'].'</pre><pre>'.$item['description'].'</pre></a><a class="space"></a><pre class="space">'.$item['date'].'</pre>'.$code.'</div></div>';
}else{
echo '<div class="right"><div class="ll"><img src="'.$util->level.'/image/'.$key.'.png"/></div><div class="rr"><a href="'.$link.'"><pre class="bold gold">'.$item['title'].'</pre><pre>'.$item['description'].'</pre></a><a class="space"></a><pre class="space">'.$item['date'].'</pre>'.$code.'</div></div></li>';
if($light=='light'){$light='dark';}else{$light='light';}
//echo ' </ul><div class="clr"></div>'.<py1>requestm.adsensepaste(0,50,backend="mobile")</py>.'<ul class="two">';
echo '<div class="clr"></div><li class="adsense"><div align="center" style="width:100%;height:50px;"><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- responsive-square -->
<ins class="adsbygoogle adslot_1"
     style="display:inline-block;height:50px;"
     data-ad-client="ca-pub-8488699542117607"
     data-ad-slot="8189130995"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script></div></li>';
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
