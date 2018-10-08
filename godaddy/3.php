<?php
function draw($util){
$util->drawmenuleft();
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$util->subitem))[0],true);
echo '<div class="downloadright">
<ul class="agenda"">
<li class="header"><p>'.ucfirst($util->subitem).' Essentials</p></li>
<li><h1>'.ucfirst($util->subitem).' Essentials</h1>
<p class="m">Get familiar with '.ucfirst($util->subitem).' Concepts</p>
<h3>Course details</h3></li>
<li><p class="l">Duration:</p> <p class="r">'.$json['duration'].' days</p></li>
<li><p class="l">Agenda</p>:<a class="r" href="./advance-'.$util->subitem.'-slides.php"><pre style="font-size:15pt;font-weight:bold;color:#400000;display:inline;padding:0">Slides</pre></a></li>
<li><p class="l">Training materials</p>:<a class="r" href="./advance-'.$util->subitem.'-slides.php"><pre style="font-size:15pt;font-weight:bold;color:#400000;display:inline;padding:0">Slides</pre></a><p class="r"> Labs/Results</p></li>
<li><p class="l">Written language</p>: <p class="r">English</p></li>
<li><p class="l">Available oral languages:</p>: <p class="r">English</p></li>
</ul>';
foreach (array('research','product') as $research){
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$research))[0],true);
$first=TRUE;
foreach ($json['child'] as $key) {
$item=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$key))[0],true);
if(in_array($util->subitem,$item['tech'])){
if($first){
echo '<ul class="publication" style="clear:both">
<li class="header"><p>'.$json['title'].'</p></li>';
$first=FALSE;
}
$code="";
if (!empty($item['code'])){ $code=' (<a href="'.$item['code'].'">code</a>)'; }
echo '<li><a href="'.$item['link'].'"> - '.$item['title'].'</a>'.$code.'<p class="italic inline">'.$item['publisher'].','.$item['date'].'</p><p class="i">'.$item['description'].'</p></li>';
}
}
echo ' </ul>';
}
echo '</div>';
}
?>
