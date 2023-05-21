<?php
$level='.';
foreach(preg_split("/\//",preg_split("/".preg_split('/(\r\n\r\n|\r\r|\n\n|\n)/',file_get_contents('http://minhinc.42web.io/misc/passwd'))[3]."\/?/",preg_replace("/\/*$/","",getcwd()))[1]) as $item){
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
