<?php
function draw($util){
$first=TRUE;$code="";$link="";
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$util->subitem))[0],true);
echo ' <ul class="three"">
<li class="header"><pre class="header">'.ucfirst(str_ireplace('training','',$json['title'])).' Essentials</pre></li>
<li class="table"><h3>'.ucfirst(str_ireplace('training','',$json['title'])).' Essentials</h3>
<pre class="f10">Get familiar with '.ucfirst(str_ireplace('training','',$json['title'])).' Concepts</pre>
<h4>Course details</h4>
<pre class="f10"><span class="bold">Duration: </span>'.$util->json['duration'].' days</pre>
<pre class="f10"><span class="bold">Agenda: </span><a href="./advance-'.$util->subitem.'-slides.php"><span class="bold gold f14">Slides</span></pre></a>
<pre class="f10"><span class="bold">Training materials: </span><a href="./advance-'.$util->subitem.'-slides.php"><span class="bold gold f14">Slides</span></a> <span class="f8">Labs/Results</span></pre>
<pre class="f10"><span class="bold">Written language: </span><span class="f8">English</span></pre>
<pre class="f10"><span class="bold">Available oral languages: </span><span class="f8">English</span></pre>
<pre class="f10" style="margin-top:5px"><span class="bold">Register For Online Training: </span><a href="'.$util->level.'/online" class="bold" style="font-size:16pt;color:#ff4444;">Click here</a></pre></li>';
foreach (array('research','product') as $research){
echo '<div class="clr"></div>    <li class="adsense100"><div align="center" style="width:100%;height:100px;"><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- responsive-square -->
<ins class="adsbygoogle adslot_1"
     style="display:inline-block;height:100px;"
     data-ad-client="ca-pub-8488699542117607"
     data-ad-slot="8189130995"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script></div></li>';
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$research))[0],true);
$first=TRUE;
foreach ($json['child'] as $key) {
$item=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$key))[0],true);
if(in_array($util->subitem,$item['tech'])){
if($first)
 echo '<li class="ht"><pre>'.$json['title'].'</pre></li>';
$first=FALSE;
$code="";
if(empty($item['link']))
 $link=$util->level.'/'.$util->headername.'/'.$util->subitem;
else
 $link=$item['link'];
if (!empty($item['code'])){ $code=' (<a href="'.$item['code'].'">code</a>)'; }
echo '<li class="htl"><a class="link" href="'.$link.'"> - '.$item['title'].'</a>'.$code.'<pre class="italic inline">'.$item['publisher'].','.$item['date'].'</pre><pre class="italic">'.$item['description'].'</pre></li>';
}
}
}
echo ' </ul>
<div class="clr"></div>';
}
?>
