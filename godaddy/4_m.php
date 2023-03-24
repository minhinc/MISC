<?php
function draw($util){
$first=TRUE;
echo '<ul class="four">
<li class="header"><pre class="header">Screenshots</pre></li>';
foreach($util->json['image'] as $key){
if($first){
echo '<li><div class="l"><img src="'.$util->level.'/image/'.$key.'"/></div>';
}else{
echo '<div class="right"><img src="'.$util->level.'/image/'.$key.'"/></div></li>';
}
$first=!$first;
}
if(!$first){
echo '</li>';
}
echo '<li class="dnld"><pre class="header">Download</pre></li>';
echo '<li class="bit"><pre class="bold center">32bit</pre></li>
<li class="zip"><pre class="l">installer(MB)</pre><pre class="right">zip(MB)</pre></li>';
if(!empty($util->json['download'])){
echo '<li class="os"><div><pre>Windows 7</pre></div><div class="zip"><pre class="l bold"><a href="'.$util->level.'/binary/'.$util->json['download']['win32'][0].'">'.$util->json['download']['win32'][0].'</a></pre><pre class="right bold"><a href="'.$util->level.'/binary/'.$util->json['download']['win32'][1].'">'.$util->json['download']['win32'][1].'</a></pre></div></li>';
}
echo ' </ul>
<div class="clr"></div>';
}
?>
