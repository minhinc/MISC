<?php
if (isset($_GET['email'])) {
$to = "sales@minhinc.com";
$from = $_GET['email'];
$message = "unsubscribe " . $from;
$headers = "From:" . $from;
$subject = "unsubscription request";
mail($to,$subject,$message,$headers);
$fn="blocked.txt";
$file=fopen($fn,"a+");
fwrite($file,"\n");
fwrite($file,$from);
fclose($file);
include "unsubscribe.html";
}
?>
