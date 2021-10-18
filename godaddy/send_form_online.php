<?php
require_once('utillib.php');
if(isset($_POST['submit'])){
$errorstring="";
$errorstring.=googlerecaptchav2();
if (preg_match('/<e>/i',$errorstring)){
 echo $errorstring.'<id>captchaid</id>';
 exit;
}

//session_start();
 $email_exp = '/^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$/';
 if(!preg_match($email_exp,$_POST['email'])) {
  $errorstring.='<id>emailid</id>';
  $errorstring.="<e><p style=\"color:#ff0000\">Wrong Email Address.</p></e>";
 }
 if(strlen($_POST['message']) < 2) {
  $errorstring.="<id>messageid</id>";
  $errorstring.="<e><p style=\"color:#ff0000\">Message Incomplete.</p></e>";
 } 
 if(preg_match('/\b(sex.*?|juicy|girl.*?|fuck.*?|wom.n.*?)\b/i',$_POST['message'])){
  $errorstring.="<e><p><span style=\"color:#ff0000\">obsenes found</span><span>mailto sales@minhinc.com</span></p></e>";
 }
 if(empty($_POST['tdate'])){
  $errorstring.="<id>dateid</id>";
  $errorstring.="<e><p style=\"color:#ff0000\">Date Missing</p></e>";
 }elseif (strtotime($_POST['tdate'])<strtotime("now")){
  $errorstring.='<id>dateid</id>';
  $errorstring.='<e><p style="color:#ff0000;">Back date selected</p></e>';
 }
 if ($errorstring!=""){
  echo $errorstring;
  exit;
 }
 $message2 = "*** Copy of your training request: ***\n\nTechnology:".$_POST['technology']."\tRequest date : ".$_POST['tdate']."\nComment :\n".$_POST['message']."\n\n+91 9483160610\nwww.minhinc.com";
 $message = "*** Training Request Submission ***\nEmail : " . $_POST['email'] . "\tName : " . $_POST['name']."\tTechnology:".$_POST['technology']."\tRequest date:".$_POST['tdate']."\nComment:\n".$_POST['message'];
 if($_FILES["attachment"]["error"] == UPLOAD_ERR_OK){
  move_uploaded_file($_FILES["attachment"]["tmp_name"], "../career/upload/" . $_FILES["attachment"]["name"]);
  $errorstring=validateattachment($_FILES["attachment"]["name"],$_FILES["attachment"]["size"],$_FILES["attachment"]["type"]);
  if(preg_match('/<e>/',$errorstring)){
   $errorstring.="<id>attachmentid</id>";
   echo $errorstring;
   exit;
  }
  $errorstring.=mail_attachment($_FILES["attachment"]["name"], "../career/upload/", "sales@minhinc.com", $_POST['email'], $_POST['email'], $_POST['email'], "*** Training request submission ***", $message);
  if(preg_match('/<e>/',$errorstring)){
   $errorstring.="<id>emailid</id>";
   echo $errorstring;
   exit;
  }
  mail_attachment($_FILES["attachment"]["name"], "../career/upload/", $_POST['email'],'sales@minhinc.com','sales@minhinc.com', 'sales@minhinc.com', "*** Training request submission copy ***", $message2);
  echo '<p style="color:#004000">Message Sent</p>';
 } else {
  $headers = "From:" . $_POST['email'];
  $headers2 = "From:" . 'sales@minhinc.com';
  $errorstring.=mail('sales@minhinc.com','*** Training request ***',$message,$headers);
  if(preg_match('/<e>/',$errorstring)){
   $errorstring.="<id>emailid</id>";
   echo $errorstring;
   exit;
  }
  mail($_POST['email'],'*** Copy of Training request ***',$message2,$headers2); // sends a copy of the message to the sender
  echo '<p style="color:#004000">Message Sent</p>';
 }
}
?>
