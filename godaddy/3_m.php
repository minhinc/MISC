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
<pre class="f10"><span class="bold">Available oral languages: </span><span class="f8">English</span></pre></li>';
foreach (array('research','product') as $research){
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
