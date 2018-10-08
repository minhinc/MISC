<?php
$level='.';
foreach(split("\/",split("public_html\/?",ereg_replace("\/*$","",getcwd()))[1]) as $item){
if(!empty($item)){
  $level=$level."/..";
 }
}
require_once($level.'/php/Mobile_Detect.php');
$platform=new Mobile_Detect;
$util;
if($platform->isMobile()){
require_once($level.'/php/Utilm_m.php');
$util=new Utilc_m;
}else{
require_once($level.'/php/Utilm.php');
$util=new Utilc;
}
?>
